from os import path
from lib.color import *
import pygame

class GameInstance(object):

	def __init__(self, **kwargs):	
		pygame.init()
		
		self.init_logo()
		
		self.player_name = kwargs.get("player_name", "CatJones")
		
		self.theme = kwargs.get("theme", "day")

		self.size = 4
		self.temporary_zoom = False
		
		self.init_fonts()
	
		self.box_size = box_size_lookup(self.size)

		self.init_player(kwargs.get("character_name", "cat"))
		
		self.clock = pygame.time.Clock()
		self.current_fps = 0
		
		
		
		self.view_max_x, self.view_max_y = view_size_lookup(self.size)
		
		pixels_x = 1000
		pixels_y = 1000
		self.init_display(pixels_x, pixels_y)
		
		self.init_map(kwargs.get("starting_map", "world", ), kwargs.get("load", "yes"), kwargs.get("round_world", True))
		
		self.display_type = kwargs.get("display_type", "text")
		
		mode = "A"
		self.init_mode(mode, kwargs.get("edit", "edit"))
		
		self.current_animations = []
	
	def init_logo(self, logo_location = "logo.png", game_name = "Text the Game"): 
		self.logo = pygame.image.load(logo_location)
		pygame.display.set_icon(self.logo)
		pygame.display.set_caption(game_name)
		
	def init_fonts(self, font="Arial Monospaced" ):
		self.font_set = []
		self.rendered_fonts = []
		for i in range(0,  NUM_SIZES):
			cur_font = pygame.font.SysFont(font, font_size_lookup(i), True)
			self.font_set.append(cur_font)
			self.rendered_fonts.append({})
			for char in char_list:
				colors = char_lookup(self.theme, char)
				self.rendered_fonts[i][char] = (cur_font.render(char, True, color_lookup(colors[0])), color_lookup(colors[1]))
	
	def change_zoom(self, new_size):
		if not(new_size < 0) and not(new_size >= NUM_SIZES):
			self.size = new_size
			self.view_max_x, self.view_max_y = view_size_lookup(self.size)
			self.box_size = box_size_lookup(self.size)
		
	def modify_zoom(self, difference):
		new_size = self.size + difference
		if not(new_size < 0) and not(new_size >= NUM_SIZES):
			self.size = new_size
			self.view_max_x, self.view_max_y = view_size_lookup(self.size)
			self.box_size = box_size_lookup(self.size)
		
	def init_player(self, character_name, move_speed=50):
		self.player_health = "FULL HEALTH"
		self.player_cash = 0
		self.player_last_move_time = 0
		self.player_level = 1
		self.player_move_speed = move_speed
		self.direction = "DOWN"
		self.current_action = "WALK"
		self.is_indoors = False
		
		self.font_image = self.rendered_fonts[0]['@'][0]
		
		self.player_images = {}
		
		print("Initializing player character as {}".format(character_name))
		for action in ACTIONS:
			self.player_images[action] = {}
			for direction in DIRECTIONS:
				self.player_images[action][direction] = {"FULL":None}
				if character_check(character_name):
					self.player_images[action][direction]["FULL"]	= pygame.image.load("./sprites/player/{}_{}_{}.png".format(character_name, action.lower(), direction.lower()))
				else: self.player_images[action][direction]["FULL"] = self.font_image
				for size in range(NUM_SIZES):
					if character_check(character_name):
						self.player_images[action][direction][size]		=  pygame.transform.scale(self.player_images[action][direction]["FULL"], box_size_lookup(size))
					else: self.player_images[action][direction][size] 	= self.font_image
		
		self.setup_abilities()
	
	#Returns the correct player image
	def lookup_player_image(self):
		return self.player_images[self.current_action][self.direction][self.size]
	
	#Returns the sprite for a character
	def lookup_map_image(self, char):
		return self.map_images[char][self.layer][self.size]
	
	
	def setup_abilities(self):
		self.abilities = {}
		
		self.abilities["SWIM_SHALLOW"] 	= True
		self.abilities["SWIM_DEEP"] 	= True
		self.abilities["CLIMB_HILL"] 	= True
		self.abilities["CLIMB_MOUNT"]	= True
		self.abilities["CLIMB_ICE_MNT"]	= True
	
	def init_display(self, pixels_x, pixels_y):
		self.screen_x = pixels_x
		self.screen_y = pixels_y
		self.aspect_ratio = pixels_x / pixels_y
		self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
	
	def init_map(self, map_name="protomap", load="yes", round_world=True):
		
		self.map = {}
		self.map["NAME"] = map_name
		self.layer = "WORLD"
		self.previous_layer = "WORLD"

		self.load_map_images()
		
		if load == "yes":	map_string = "saves/{}_{}".format(self.player_name, self.map["NAME"])
		else:				map_string = "maps/{}".format(map_name)
		#self.outside_space = self.rendered_fonts[self.size]['=']	
																
		self.round_world = round_world
		
		for layer in MAP_LAYERS:
			map_filepath = "{}_{}".format(map_string, layer)
			self.map[layer] = load_map(map_filepath, "txt")
		#self.render_map()
		self.map["SIZE_X"] = len(self.map["WORLD"]) #Map width
		self.map["SIZE_Y"] = len(self.map["WORLD"][0])  #map height
		print("map size is {} x {}".format(self.map["SIZE_X"], self.map["SIZE_Y"]))
		
		#Place the player
		self.place_player()
		
		self.new_view = True
	
	def load_map_images(self):
		self.map_images = {}
		#Load in sprites 
		for char in char_list:
			#Determine character unique string
			char_str = unfriendly_char_substitutes(char) if char in unfriendly_chars else char
			self.map_images[char] = {}
			
			for layer in MAP_LAYERS:
				#Uncomment this when you are ready to add the layers
				#file_name = "./sprites/map/{}{}.png".format(char_str, '_'+layer if layer!='WORLD' else "")
				file_name = "./sprites/map/{}.png".format(char_str)
				
				self.map_images[char][layer] = {}
				self.map_images[char][layer]["DEFAULT_SIZE"] = pygame.image.load(file_name)
				
				for size in range(NUM_SIZES):
					img = pygame.transform.scale(self.map_images[char][layer]["DEFAULT_SIZE"] , box_size_lookup(size))
					self.map_images[char][layer][size] = img
			
	
	def take_action(self):
		curr_char = self.get_char()
		next_char = self.get_char_in_front()
		
		
		swimming  = self.is_swimming()									
		water = (next_char == 'w' or next_char == 'W')
		can_walk_here  = (next_char not in self.char_no_walk)	
		walking  = self.is_walking()
		on_mount = (curr_char == 'M' or curr_char == 'm' or curr_char == '^')
		mount_next = False
		if (next_char == 'M' or next_char == 'm' or next_char == '^'):
			if next_char == 'm' and self.abilities["CLIMB_HILL"]:
				mount_next = True
			if next_char == 'M' and self.abilities["CLIMB_MOUNT"]:
				mount_next = True
			if next_char == '^' and self.abilities["CLIMB_ICE_MNT"]:
				mount_next = True
		sit = (next_char == 'c') or (curr_char == 'c' and can_walk_here) 
		door = (next_char == 'D')
		up = (next_char == '>')
		down = (next_char == '<')
		layer_change = (is_layer(next_char))
		
		#Going in/out of water
		if (not swimming and water) or (swimming and can_walk_here):	
			self.toggle_swimming()	
		
		#Mountain climbing 
		elif (on_mount and can_walk_here) or mount_next:				
			self.adjust_location()	
		
		#Sitting
		elif sit:						
			self.adjust_location()	
		
		#Going in or outdoors
		elif door:					
			self.toggle_indoors()	
		
		#Going up a layer
		elif up: 																				
			self.adjust_location()
			self.change_layer(ascend(self.layer))
														
		#Going down a layer
		elif down:																				
			self.adjust_location()
			self.change_layer(descend(self.layer))
		
		#Numbered door for changing layers	
		elif layer_change:																								
			self.adjust_location()
			self.change_layer(MAP_LAYERS[int(next_char)])
														
		
	def is_executing(self):
		return self.game_is_executing
	
	def init_mode(self, mode = 'A', allow_editing = "no-edit"):
		self.mode = mode
		self.char_no_walk = []
		if allow_editing == "edit": self.edit_enabled = True
		else:						self.edit_enabled = False
		self.edit_char = ' '
		
		if mode is 'A':
			#Active mode
			self.char_no_walk = COLLISION_CHARS

		if mode is 'P':
			#Platform mode
			self.char_no_walk = ['/', '\\', '|', '-', "#"]
			
		self.game_is_executing = True
		self.detect_collision = True
		self.edit_mode = False
	
	def save(self, save_param = "current"):
		if save_param == "current":
			save_loc = "saves/{}_{}_{}".format(self.player_name, self.map["NAME"], self.layer)
			print(save_loc)
			save_map(save_loc, self.map[self.layer])
		else:
			for layer in MAP_LAYERS:
				save_loc = "saves/{}_{}_{}".format(self.player_name, self.map["NAME"], layer)
				print(save_loc)
				save_map(save_loc, self.map[layer])
		
	
	def quit(self):
		self.game_is_executing = False
		
	def get_char(self):
		return self.map[self.layer][self.player_x][self.player_y]
		
	def set_char(self, c):	
		self.map[self.layer][self.player_x][self.player_y] = c
	
	def set_char_to_edit(self):
		self.map[self.layer][self.player_x][self.player_y] = self.edit_char

	def get_mode(self):
		return self.mode
		
	def tick(self, max_fps=30):
		self.current_fps = self.clock.get_time()
		self.clock.tick(max_fps)	
		
	def place_player(self):
		for y in range(self.map["SIZE_Y"]):
			for x in range(self.map["SIZE_X"]):
				if self.map[self.layer][x][y] == 'S':
					self.player_x = x
					self.player_y = y					
	
	def set_edit_char(self, edit_key, is_upper=False):
		edit_char = pygame.key.name(edit_key)
		if edit_char == "space" : 					self.edit_char = ' '							#Space
		elif is_upper:
			if edit_char.isalpha():					self.edit_char = edit_char.upper() 				#Shift + Letter
			elif edit_char.isdigit(): 				self.edit_char = lookup_symbol_upper(edit_char)	#Shift + Number
			elif edit_char in valid_symbols: 		self.edit_char = lookup_symbol_upper(edit_char)	#Shift + Symbol
		else:										self.edit_char = edit_char						#No shift

	def can_walk(self):
		if self.get_char_in_front() in self.char_no_walk: return False
		else: return True
		
	def get_char_in_front(self):
		lookup = {
		"UP"	:	self.map[self.layer][self.player_x][(self.player_y - 1) % self.map["SIZE_Y"]],
		"DOWN"	:	self.map[self.layer][self.player_x][(self.player_y + 1) % self.map["SIZE_Y"]],
		"LEFT"	:	self.map[self.layer][(self.player_x - 1) % self.map["SIZE_X"]][self.player_y],
		"RIGHT"	:	self.map[self.layer][(self.player_x + 1) % self.map["SIZE_X"]][self.player_y]
		}
		return lookup.get(self.direction, " ")
	
	def get_loc_in_front(self):
		lookup = {
		"UP"	:	(self.player_x, ((self.player_y - 1) % self.map["SIZE_Y"])),
		"DOWN"	:	(self.player_x, ((self.player_y + 1) % self.map["SIZE_Y"])),
		"LEFT"	:	(((self.player_x - 1) % self.map["SIZE_X"]), self.player_y),
		"RIGHT"	:	(((self.player_x + 1) % self.map["SIZE_X"]), self.player_y)
		}
		return lookup.get(self.direction, (self.player_x, self.player_y))
	
	def next_frame(self, latest_key=pygame.K_DOWN):
		player_x, player_y = 0,0
	
		#Clear the screen
		self.screen.fill(color_lookup("DAY_SKY"))
		self.display_stats()	
			
		if self.edit_enabled and self.edit_mode:
			self.set_char_to_edit()
							
		#Render each character in view onto a surface
		for y in range(self.view_max_y):
			for x in range(self.view_max_x):
				#current_character, bg_color = self.outside_space
				
				map_x = (self.player_x - int(self.view_max_x/2) + x) % self.map["SIZE_X"]
				map_y = (self.player_y + int(self.view_max_y/2) - self.view_max_y + y) % self.map["SIZE_Y"]
				
				if self.round_world or not (map_x < 0 or map_x >= self.map["SIZE_X"] or map_y < 0 or map_y >= self.map["SIZE_Y"]): #world is round
					map_value = self.map[self.layer][map_x][map_y]
					if is_layer(map_value): map_value = 'D'
				
				if self.display_type == "sprite":
					bg_color = color_lookup(map_value)[1]
					self.blit_to_screen(self.lookup_map_image(map_value),  x, y, bg_color)
				else: 												
					current_character, bg_color = self.rendered_fonts[self.size][map_value]
					self.blit_to_screen(current_character, x, y, bg_color)
				
				#Draw the player				
				if map_x == self.player_x and map_y == self.player_y: player_x, player_y = x,y 
		self.display_player(player_x, player_y)	
		#Render on onto a surface
		pygame.display.update()
		self.new_view = False
		
		#Cap at 60 frames per second
		self.tick(60)
			
	def display_player(self, x, y):
		x_offset = 15
		y_offset = 20
		
		if 		self.at('m'): y_offset -= box_size_lookup(self.size)[1] * .10
		elif 	self.at('#'): y_offset += box_size_lookup(self.size)[1] * .05
		
		screen_x = self.box_size[1]*self.aspect_ratio*x + x_offset
		screen_y = self.box_size[1]*y + y_offset
		
		self.screen.blit(self.lookup_player_image(), (screen_x,screen_y))

	def display_stats(self):
		player_loc = "Player at " + str(self.player_x) + ", " + str(self.player_y)
		status = self.font_set[3].render(player_loc, True, color_lookup("BRIGHTGREEN"))
		self.screen.blit(status, ((10),(10)))
		 
		health = self.font_set[3].render("{}".format(self.player_health), True, color_lookup("BRIGHTGREEN"), color_lookup("RED"))
		self.screen.blit(health, ((self.screen_x*.2),10))
		
		misc = self.font_set[3].render("LAYER: {}    ${}    MOVESPEED:{}".format(str(self.map["NAME"]), self.player_cash, self.player_move_speed), True, color_lookup("BRIGHTGREEN"))
		self.screen.blit(misc, ((self.screen_x*.4),10))
		
		status = self.font_set[3].render(("FPS:"+str(self.current_fps)), True, color_lookup("BRIGHTGREEN"))
		self.screen.blit(status, ((self.screen_x*.9),10))		
		
	def blit_to_screen(self, char, x, y, background_color = (0,0,0)):
		#If display mode is sprite, we need a 4px modifier 
		z = 4 if self.display_type == "sprite" else 0
		
		padding = self.box_size[1]
		#draw rectangle
		pygame.draw.rect(self.screen, background_color, ((padding*self.aspect_ratio*x+15 +z),(padding*y+25), self.box_size[0], self.box_size[1]), 0)

		self.screen.blit(char, ((padding*self.aspect_ratio*x+15+4),(padding*y+25)))
 	
	def process_movement(self, p_up = False, p_down = False, p_left = False, p_right = False):
		if pygame.time.get_ticks() - self.player_last_move_time > self.player_move_speed:	
			if p_up is True:	self.move_player("UP")
			if p_down is True:	self.move_player("DOWN")
			if p_left is True:	self.move_player("LEFT")
			if p_right is True:	self.move_player("RIGHT")

			self.player_last_move_time = pygame.time.get_ticks()
			self.check_area()
			
	def adjust_location(self):
		self.player_x, self.player_y = self.get_loc_in_front()
		
		self.new_view = True
	
	def move_player(self, direction, spaces = 1):
		self.direction = direction
		going_to_walk = (self.can_walk() and self.current_action is "WALK")					#Walking
		collision_detection_is_off = (not self.detect_collision)							#Collision detection is off
		going_to_swim = False
		if self.current_action is "SWIM":													#Swimming
			if 		self.get_char_in_front() == 'w' and self.abilities["SWIM_SHALLOW"]: 	going_to_swim = True
			elif 	self.get_char_in_front() == 'W' and self.abilities["SWIM_DEEP"]: 		going_to_swim = True
		on_a_mountain = self.temporary_zoom													#Mountain Climbing
		
		for space in range(spaces):
			if ((going_to_walk or going_to_swim) and not on_a_mountain) or collision_detection_is_off:
				self.adjust_location()
		
	
	def throw_spear():
		if self.inventory("spear"):
			self.isAnimated = True
			#animate_spear()
		else:
			self.isAnimated = False
	
	def at(self, char):
		return self.get_char() is char
	
	def check_area(self):		
		if self.temporary_zoom: 
			self.temporary_zoom = False
			self.change_zoom(4)
			
	
		if self.detect_collision:
			#See more from hills
			if self.at('m'):					
				self.change_zoom(3)
				self.temporary_zoom = True
			
			#See far from mountains
			elif self.at('M'):					
				self.change_zoom(2)
				self.temporary_zoom = True
			
			#See farthest from the highest peaks			
			elif self.at('^'):					
				self.change_zoom(1)
				self.temporary_zoom = True
			
			#Slide on ice			
			elif self.at('x'):					
				self.player_last_move_time += self.player_move_speed * 2
				self.adjust_location()
	
			#Collect cash
			elif self.at('$'):					
				self.player_cash += 1
				self.set_char(' ')
			
			#These will hurt you
			elif self.at('*'):					
				self.change_player_health(-1)
				self.set_char(' ')
				
			#Lave hurts more
			elif self.at('l') or self.at('L'): 	
				self.change_player_health(-3)
				self.move_player(opposite_direction(self.direction))
				self.flash()
			
			#If in water and not swimming (Edge case?)
			elif (self.at('w') or self.at('W')) and not self.is_swimming:
				print("doing this")
				self.toggle_swimming()
			
			
	def flash(self):
		self.screen.fill((255, 0, 0))
		pygame.display.update()
		pygame.time.delay(120)
		
			
	def load_new_map(self, map_name="1"):	
		#self.player_level += 1
		self.map = self.init_map(map_name)
		self.next_frame()

	def change_player_health(self, modifier=0):
		length = len(self.player_health)
		if length + modifier <= 0:
			print("You died! ='(")
			self.quit()
		elif length + modifier >= 16: 
			self.player_health = "PLAYER HEALTH+++"
		elif modifier < 0:
			self.player_health = self.player_health[:(length+modifier)]
		else:
			self.player_health += "+"

	def change_player_move_speed(self, modifier=0):
		self.player_move_speed += modifier

	def change_layer(self, new_layer):
		#self.previous_layer = self.layer
		self.layer = new_layer
		
	def toggle_indoors(self):
		temp_layer = self.previous_layer
		if self.is_indoors: 
								self.previous_layer = self.layer
								self.change_layer(temp_layer)
								
		else:					
								self.previous_layer = self.layer
								self.change_layer("INDOORS")
								
		self.is_indoors = not self.is_indoors

								
								
	
	def is_indoors(self):
		return self.is_indoors
		
	def toggle_swimming(self):
		self.player_x, self.player_y = self.get_loc_in_front()
		if self.current_action is "WALK":	self.current_action = "SWIM"
		else:								self.current_action = "WALK"
		
	def is_walking(self):
		if self.current_action is "WALK": return True
		else: return False
		
	def is_swimming(self):
		if self.current_action is "SWIM": return True
		else: return False
		
	def toggle_collision(self):
		self.detect_collision = not self.detect_collision
		
	def toggle_editmode(self):
		self.edit_mode = not self.edit_mode
	
	def is_edit(self):
		return self.edit_mode
		
	def can_edit(self):
		return self.edit_enabled
	
	def create_blank_layers(self):
		generate_map_layers(self.map["WORLD"])
		
def opposite_direction(direction):
	lookup = {
	"UP"	:	"DOWN",
	"DOWN"	:	"UP",
	"LEFT"	:	"RIGHT",
	"RIGHT"	:	"LEFT"
	}
	return lookup.get(direction, "DOWN")
	
	
def save_map(name, map, format = "txt"):
		"""
		calculate length and width of a square 
		that fits inside the map in order to 
		support maps with any shape
		"""
		
		file_location = str(name) + '.' + format
		os = "Windows"
		
		map_size_y = len(map[0])
		map_size_x = len(map)
		
		if format is "txt":											#Notepad
			
			#if not path.isfile(file_location):						#Verify that you are not overwriting anything
			with open(file_location, 'w') as output_file:
				#Loop through map
				for y in range(map_size_y):
					for x in range(map_size_x):
						output_file.write(map[x][y])
					if os is "Windows":								#May need to add platform dependent logic here

						output_file.write('\n')
					else:
						output_file.write('\n')
			output_file.close()
				
		#Compressed for production version
		if format is "yml":
			return False
		else:
			return False
			
def load_map(name, format = "txt"):
	file_location = "{}.{}".format(str(name), format)
	os = "Windows"
	temp_map = []
	map = []

	#Notepad
	if format is "txt":
		#Verify that the file exists
		if path.isfile(file_location):
			temp_map = [y for y in list([x.rstrip() for x in open(file_location,"r")])]
			map = [list(i) for i in zip(*temp_map)]	
			return map
		else:
			return False
	return False


	
def generate_map_layers(map, format="txt"):
	os = "windows"
	
	base_location = "maps/MAP_LAYER"
	file_location = ""
	
	
	world_size_y = len(map[0])
	world_size_x = len(map)
	
	if format is "txt":												#Notepad
		for layer in MAP_LAYERS:
			file_location = "{}_{}.{}".format(base_location, layer, format)
			with open(file_location, 'w') as output_file:
				for y in range(world_size_y):							#Loop through map
					for x in range(world_size_x):
						char = map[x][y]
						if layer is "WORLD":			output_file.write(map[x][y])
						elif char in building_pieces:	output_file.write('%')
						elif char is 'd':				output_file.write('d')
						elif char is 'S':				output_file.write('S')
						else:							output_file.write('#')
					if os is "Windows":								#May need to add platform dependent logic here
						output_file.write('\n')
					else:
						output_file.write('\n')
			output_file.close()
	
"""	
class animation(object):
	def __init__(num_frames=0, image=None, starting_location=(0,0), direction='UP'):
		self.num_frames = num_frames
		
What might need to be animated?...
	Projectiles thrown by character or enemies (* moving across the screen)
	Changes made to the map (ie. earth quakes, lava flowing, buildings being created, water flowing etc...)
	
	I will need to think about how this should be implemented

"""		