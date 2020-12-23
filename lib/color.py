DIRECTIONS 		= ["UP","DOWN","LEFT","RIGHT"]
ACTIONS			= ["WALK", "SWIM"]
MAP_LAYERS		= ["WORLD", "INDOORS", "GROUND_1", "GROUND_2", "SKY_1", "SKY_2"]
COLLISION_CHARS = ['0', '1', '2', '3', '4', '5', 'D', 'N', 'c', 'm', 'w', '^', 't', 'T', 'X', 'I', '=','M', 
										'W', '/', '\\', '|', '-', '!', '<', '>']
									
def is_layer(char):
	if char in ['0','1','2','3','4','5']: 	return True
	else:									return False

def game_items(item_name):
	lookup = {
	"spear" : False
	}
	return lookup.get(item_name, False)
	
def descend(layer):
	lookup = {
	"WORLD"		: "GROUND_1",
	"SKY_2"		: "SKY_1",
	"SKY_1"		: "INDOORS",
	"INDOORS" 	: "GROUND_1",
	"GROUND_1"	: "GROUND_2",
	"GROUND_2"	: "GROUND_2"
	}
	return lookup.get(layer, "WORLD")
	
def ascend(layer):
	lookup = {
	"WORLD"		: "SKY_1",
	"GROUND_2"	: "GROUND_1",
	"GROUND_1"	: "INDOORS",
	"INDOORS"	: "SKY_1",
	"SKY_1"		: "SKY_2",
	"SKY_2"		: "SKY_2",
	}
	return lookup.get(layer, "WORLD")
	
def character_check(char_name):
	lookup = {
	"cat" : True
	}
	return lookup.get(char_name, False)

NUM_SIZES = 7	
	
def box_size_lookup(size):
	lookup = {
	0	:	(11, 8),
	1	:	(16, 14),
	2	:	(22, 18),
	3	:	(29, 26),
	4	:	(32, 29),
	5	:	(43, 32),
	6	:	(55, 40)
	}
	return lookup.get(size, (22, 16))
	
def view_size_lookup(size):
	lookup = {
	0	:	(121, 121),
	1	:	(69, 69),
	2	:	(54, 54),
	3	:	(37, 37),
	4	:	(33, 33),
	5	:	(30, 30),
	6	:	(24, 24)
}
	return lookup.get(size, (33, 33))

def font_size_lookup(size):
	lookup = {
	0	:	5,
	1	:	10,
	2	:	15,
	3	:	18,
	4	:	30,
	5	:	40,
	6	:	50
	}
	return lookup.get(size, 20)


	
char_list = [
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
	'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
	'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
	'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
	'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
	'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
	'W', 'X', 'Y', 'Z', '1', '2', '3', '4',
	'5', '6', '7', '8', '9', '0', '`', '~',
	'!', '@', '#', '$', '%', '^', '&', '*',
	'(', ')', '<', '>', ',', '.', '?', '/',
	'|', '\\', ']', '[', '{', '}', '-', '_',
	'+', '=', ' ', ';', ':', '\'', '"'
]

#This is the list of chars which cannot be used in filenames in a windows system
unfriendly_chars = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
	'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	'*', '<', '>', '|', ' ', '?', '/', '\\', ';', ':', '`', '\'', '"'
]
def unfriendly_char_substitutes(symbol):
	lookup = {
		'A'	: 'CAP_A', 
		'B'	: 'CAP_B',
		'C'	: 'CAP_C', 
		'D'	: 'CAP_D', 
		'E'	: 'CAP_E', 
		'F'		: 'CAP_F', 
		'G'	: 'CAP_G', 
		'H'	: 'CAP_H', 
		'I'		: 'CAP_I', 
		'J'		: 'CAP_J', 
		'K'	: 'CAP_K', 
		'L'		: 'CAP_L', 
		'M'	: 'CAP_M', 
		'N'	: 'CAP_N', 
		'O'	: 'CAP_O', 
		'P'	: 'CAP_P', 
		'Q'	: 'CAP_Q', 
		'R'	: 'CAP_R', 
		'S'	: 'CAP_S', 
		'T'		: 'CAP_T', 
		'U'	: 'CAP_U', 
		'V'	: 'CAP_V', 
		'W'	: 'CAP_W', 
		'X'	: 'CAP_X', 
		'Y'		: 'CAP_Y', 
		'Z'	: 'CAP_Z',
		'*'	: 'SYM_AST',
		'>'	: 'SYM_GT',
		'<'	: 'SYM_LS',
		'|'		: 'SYM_OR',
		' '		: 'SYM_SP',
		'?'		: 'SYM_QU',
		'\\'	: 'SYM_BSL',
		'/'		: 'SYM_FSL',
		';'		: 'SYM_SC',
		':'		: 'SYM_C',
		'`'	: 'SYM_AP',
		'\''	: 'SYM_SQ',
		'"'		: 'SYM_DQ'
		
	}
	return lookup.get(symbol, symbol)
	

valid_symbols = [',','.','/','[',']',';','\',','\\','-','=','`']

building_pieces = ['I', '=', '~', '!'
]
def lookup_symbol_upper(symbol):
	lookup = {
		',' : '<',
		'.' : '>',
		'/' : '?',
		';' : ':',
		'\'' : '"',
		'[' : '{',
		']' : '}',
		'\\' : '|',
		'`' : '~',
		'-' : '_',
		'=' : '+',
		'1' : '!',
		'2' : '@',
		'3' : '#',
		'4' : '$',
		'5' : '%',
		'6' : '^',
		'7' : '&',
		'8' : '*',
		'9' : '(',
		'0' : ')'	
	}
	return lookup.get(symbol, '.')
	
def color_lookup(color):
	lookup = {
		"WHITE" 		: (255, 255, 255),
		"RED" 			: (255, 0, 0),
		"MAROON"		: (100, 0, 10),
		"DARKGREEN"		: (30, 150, 30),
		"GREEN"			: (0, 255, 0),
		"MEDIUMGREEN"	: (15, 155, 50),
		"MILDGREEN"		: (60, 200, 60),
		"LIGHTGREEN" 	: (70, 211, 70),
		"BLUE"			: (0, 0, 255),
		"MILDBLUE" 		: (50,50,255),
		"LIGHTBLUE" 	: (240,248,255),
		"BLACK" 		: (0, 0, 0),
		"PLAYER" 		: (145, 250, 155),
		"BRIGHTGREEN" 	: (175, 255, 175),
		"SUNSETPINK" 	: (255,170,196),
		"DARKBROWN"		: (55,37,22),
		"BROWN" 		: (75,52,32),
		"LIGHTBROWN" 	: (95,67,42),
		"GREY" 			: (92,92,92),
		"ORANGE" 		: (255,165,0),
		"MEDGREY"		: (120, 120, 120),
		"LIGHTGREY"		: (210, 210, 210),
		"GOLD" 			: (255,223,0),
		"DUSTY_GOLD"	: (150, 141,0),
		"NIGHT_MOUNTAIN": (55,25,7),
		"NIGHT_GROUND"	: (40,60,22),
		"NIGHT_SKY"		: (25,25,37),
		"NIGHT_SHALLOW"	: (15,20,88),
		"NIGHT_DEEP"	: (12,12,68),
		"NIGHT_GRASS"	: (15,66,12),
		"NIGHT_TREE"	: (4,77,10),
		"DAY_MOUNTAIN"	: (90,61,34),
		"DAY_GROUND"	: (122, 168, 70),
		"SHRUB"			: (177, 181, 100),
		"DAY_SKY"		: (135,206,235),
		"DAY_SHALLOW"	: (121,136,189),
		"DAY_DEEP"		: (68,87,144),
		"DAY_GRASS"		: (102,141,60),
		"DAY_MEADOW"	: (130,177,73),
		"DAY_TREE"		: (33,87,35),
		"DAY_ICE"		: (82, 111, 187),
		"FROZEN"		: (165, 185, 220),
		"APPOC_GROUND"	: (33,87,35),
		"APPOC_SKY"		: (25,25,37),
		"APPOC_SHALLOW"	: (87,36,19),
		"APPOC_DEEP"	: (55,17,22),
		"APPOC_GRASS"	: (122,101,40),
		"APPOC_TREE"	: (149,108,126),
		"DESERT_SAND"	: (237, 201, 175),
		"DESERT_BLUE"	: (216, 246, 244),
		"DESERT_OASIS"	: (175, 237, 232),
		"DESERT_CACTUS"	: (175, 237, 201),
		"DESERT_SKY"	: (237, 251, 250),
		"DESERT_CLIFF"	: (96, 62, 55),
		"DESERT_GROUND"	: (230, 187, 168),
		"DESERT_PATCH"	: (246, 229, 217),
		"DUNE"			: (240, 209, 181),
		"DESERT_WALL"	: (93, 79, 69),
		"DESERT_ROOF"	: (128, 125, 123),
		"STONE"			: (161, 161, 161),
		"LAVA_RED"		: (247, 8, 8),
		"LAVA_YELLOW"	: (255, 108, 8),
		"HAZE"			: (246, 246, 246)
	}
	return lookup.get(color, (0,0,0))

def char_lookup(theme, char):
	lookup = {
		"text"	: text_char_lookup(char),
		"night" : night_char_lookup(char),
		"day" 	: day_char_lookup(char),
		"appoc" : appoc_char_lookup(char),
		"desert": desert_char_lookup(char)
	}
	return lookup.get(theme, day_char_lookup(char))
		
def day_char_lookup(char):
	lookup = {
	'-' : ("WHITE", "DAY_GROUND"),		#Horizontal Wall
	'/' : ("WHITE", "DAY_GROUND"),		#Corner Wall 1
	'\\' : ("WHITE", "DAY_GROUND"),		#Corner Wall 2
	'|' : ("WHITE", "DAY_GROUND"),		#Vertical Wall
	'.' : ("DAY_GRASS", "DAY_GROUND"),	#Grass
	':' : ("DAY_GRASS", "DAY_MEADOW"),	#Meadow
	'['	: ("WHITE", "DAY_GRASS"),		#Bridge Left
	']' : ("WHITE", "DAY_GRASS"),		#Bridge Right
	'W' : ("DAY_SHALLOW", "DAY_DEEP"),	#Water
	'w' : ("DAY_DEEP", "DAY_SHALLOW"), 	#Reef
	'M' : ("DAY_MOUNTAIN", "DAY_GRASS"),#Mountain
	'm' : ("DAY_MOUNTAIN", "DAY_GRASS"),#Hill
	'X' : ("STONE", "BROWN"),			#Cliff
	'x' : ("DAY_ICE", "FROZEN"),		#Ice
	'#' : ("BLACK", "BLACK"),			#Hash wall
	'$' : ("GOLD", "BLACK"),			#Cash
	'l' : ("DAY_GROUND", "GOLD"),		#Spear
	'T' : ("DAY_TREE", "DAY_GROUND"),	#Large Tree
	't' : ("DAY_TREE", "DAY_GROUND"),	#Small Tree
	'F' : ("DAY_TREE", "DAY_SKY"),  	#Forest
	'_' : ("GREY", "WHITE"),			#Snow
	' ' : ("WHITE", "DAY_GRASS"),		#Field
	'D' : ("GREY", "GREY"),				#Door
	'I' : ("BROWN", "BROWN"),			#Building Wall
	'=' : ("GREY", "GREY"),				#Roof
	'S' : ("GOLD", "GOLD"),				#Start
	's' : ("DESERT_SAND", "DESERT_SAND"),#Sand
	',' : ("STONE", "STONE"),			#Gravel
	'l' : ("LAVA_RED", "LAVA_YELLOW"),	#Orange lava
	'L' : ("LAVA_YELLOW", "LAVA_RED"),	#Red lava
	'`' : ("DESERT_SAND", "DUNE"),		#Dune
	';' : ("SHRUB", "DESERT_SAND"),		#Shrub
	'\'': ("DUNE", "DESERT_GROUND"),	#Desert sand
	'!' : ("DESERT_WALL","DESERT_WALL"),#Desert building
	'~' : ("DESERT_ROOF","DESERT_ROOF"),#Desert roof
	'^' : ("DAY_ICE", "WHITE"),			#Ice Mountain
	'#' : ("BROWN", "STONE")			#Sunk in ground
	
	}
	return lookup.get(char, ("RED", "BLACK"))

		
def text_char_lookup(char):
	lookup = {
	'q'	: ("BLACK", "BLACK"),			#Underground (All black)
	'Q' : ("DAY_SKY", "DAY_SKY"),		#Sky (All blue)
	'h' : ("HAZE", "HAZE"),				#Clouds (All haze)
	'-' : ("WHITE", "DAY_GROUND"),		#Horizontal Wall
	'/' : ("WHITE", "DAY_GROUND"),		#Corner Wall 1
	'\\' : ("WHITE", "DAY_GROUND"),		#Corner Wall 2
	'|' : ("WHITE", "DAY_GROUND"),		#Vertical Wall
	'.' : ("DAY_GRASS", "DAY_GROUND"),	#Grass
	':' : ("DAY_GRASS", "DAY_MEADOW"),	#Meadow
	'['	: ("WHITE", "DAY_GRASS"),		#Bridge Left
	']' : ("WHITE", "DAY_GRASS"),		#Bridge Right
	'W' : ("DAY_SHALLOW", "DAY_DEEP"),	#Water
	'w' : ("DAY_DEEP", "DAY_SHALLOW"), 	#Reef
	'M' : ("DAY_MOUNTAIN", "DAY_GRASS"),#Mountain
	'm' : ("DAY_MOUNTAIN", "DAY_GRASS"),#Hill
	'X' : ("STONE", "BROWN"),			#Cliff
	'x' : ("DAY_ICE", "FROZEN"),		#Ice
	'#' : ("BROWN", "BLACK"),			#Sunk in ground
	'$' : ("GOLD", "BLACK"),			#Cash
	'l' : ("DAY_GROUND", "GOLD"),		#Spear
	'o' : ("STONE", "DESERT_WALL"),		#Cobblestone floor
	'T' : ("DAY_TREE", "DAY_GROUND"),	#Large Tree
	't' : ("DAY_TREE", "DAY_GROUND"),	#Small Tree
	'F' : ("DAY_TREE", "DAY_SKY"),  	#Forest
	'_' : ("GREY", "WHITE"),			#Snow
	' ' : ("WHITE", "DAY_GRASS"),		#Field
	'D' : ("GOLD", "BLACK"),			#Door
	'I' : ("MEDGREY", "GREY"),			#Building Wall
	'=' : ("LIGHTBROWN", "BROWN"),		#Roof
	'S' : ("WHITE", "GOLD"),			#Start
	's' : ("DESERT_GROUND", "DESERT_SAND"),#Sand
	',' : ("MEDGREY", "STONE"),			#Gravel
	'l' : ("LAVA_RED", "LAVA_YELLOW"),	#Orange lava
	'L' : ("LAVA_YELLOW", "LAVA_RED"),	#Red lava
	'`' : ("DESERT_SAND", "DUNE"),		#Dune
	';' : ("SHRUB", "DESERT_SAND"),		#Shrub
	'\'': ("DUNE", "DESERT_GROUND"),	#Desert sand
	'!' : ("DESERT_ROOF","DESERT_WALL"),#Desert building
	'~' : ("DESERT_WALL","DESERT_ROOF"),#Desert roof
	'^' : ("DAY_ICE", "WHITE"),			#Ice Mountain
	'<' : ("BLACK", "GREY"),			#Upstairs
	'>' : ("BLACK", "GREY"),			#Downstairs
	'N' : ("DUNE", "DESERT_GROUND"),	#Table
	'c' : ("DUNE", "STONE"),			#Chair
	'z' : ("DARKBROWN", "BROWN"),		#Dirt
	'B' : ("RED", "BLUE"),				#Bed style 1
	'i'	: ("ORANGE", "DESERT_GROUND"),	#Candle
	'8' : ("DUSTY_GOLD", "MAROON"),		#Carpet style 1
	'%' : ("MEDGREY, NIGHT_GRASS")		#Carpet style 2
	
	}
	return lookup.get(char, ("RED", "BLACK"))
	
	
def night_char_lookup(char):
	lookup = {
	'-' : ("GREY", "BLACK"),				#Horizontal Wall
	'=' : ("GREY, NIGHT_GROUND"),			#Horizontal Path
	'/' : ("GREY", "BLACK"),				#Corner Wall 1
	'\\' : ("GREY", "BLACK"),				#Corner Wall 2
	'|' : ("GREY", "BLACK"),				#Vertical Wall
	'.' : ("NIGHT_GRASS", "NIGHT_GROUND"),	#Grass
	'['	: ("GREY", "BLACK"),				#Entrance Left
	']' : ("GREY", "BLACK"),				#Entrance Right
	'W' : ("NIGHT_SKY", "NIGHT_DEEP"),		#Water
	'w' : ("NIGHT_SKY", "NIGHT_SHALLOW"), 	#Reef
	'M' : ("NIGHT_MOUNTAIN", "NIGHT_SKY"),	#Mountain
	'm' : ("NIGHT_MOUNTAIN", "NIGHT_SKY"),	#Hill
	"X" : ("BROWN", "NIGHT_GROUND"),		#Cliff
	"x" : ("NIGHT_SHALLOW", "DAY_ICE"),		#Ice
	"#" : ("SUNSETPINK", "BLACK"),			#Hash wall
	"$" : ("GOLD", "BLACK"),				#Cash
	"L" : ("BLACK", "GOLD"),				#Next Level
	"l" : ("BLACK", "GOLD"),				#Previous Level
	"T" : ("NIGHT_TREE", "NIGHT_SKY"),		#Large Tree
	"t" : ("NIGHT_TREE", "NIGHT_GROUND"),	#Small Tree
	"F" : ("NIGHT_TREE", "NIGHT_SKY"),  	#Forest
	"_" : ("GREY", "NIGHT_SKY"),			#Snow
	" " : ("WHITE", "NIGHT_GRASS"),			#Field
	"d" : ("WHITE", "WHITE"),				#Door
	"I" : ("BLACK", "LIGHTBROWN"),			#Building Wall
	'=' : ("GREY", "GREY"),					#Roof
	"S" : ("GOLD", "GOLD")					#Start
	}
	return lookup.get(char, ("RED", "BLACK"))

def desert_char_lookup(char):
	lookup = {
		'-'	: ("DESERT_WALL", "DESERT_SAND"),
		'/'	: ("DESERT_WALL", "DESERT_SAND"),
		'\\': ("DESERT_WALL", "DESERT_SAND"),
		'|'	: ("DESERT_WALL", "DESERT_SAND"),
		'.'	: ("DESERT_CACTUS", "DESERT_GROUND"),
		',' : ("DESERT_PATCH", "DESERT_PATCH"),
		'X' : ("DESERT_SAND", "DESERT_SAND"),
		'w' : ("DESERT_BLUE", "DESERT_OASIS"),
		'd' : ("BLACK", "BLACK"),
		'I' : ("DESERT_WALL", "DESERT_WALL"),
		'=' : ("DESERT_ROOF", "DESERT_ROOF"),
		'W' : ("DESERT_BLUE", "DESERT_OASIS"),
		'm' : ("DESERT_CLIFF", "DESERT_SAND"),
		'M' : ("DESERT_CLIFF", "DESERT_CLIFF"),
		'g' : ("DESERT_CACTUS", "DESERT_CACTUS")
	}
	return lookup.get(char, ("DESERT_GROUND", "DESERT_GROUND"))

	
def appoc_char_lookup(char):
	lookup = {
	'-' : ("GREY", "BLACK"),				#Horizontal Wall
	'=' : ("GREY, APPOC_GROUND"),			#Horizontal Path
	'/' : ("GREY", "BLACK"),				#Corner Wall 1
	'\\' : ("GREY", "BLACK"),				#Corner Wall 2
	'|' : ("GREY", "BLACK"),				#Vertical Wall
	'.' : ("APPOC_GRASS", "APPOC_GROUND"),	#Grass
	'['	: ("GREY", "BLACK"),				#Entrance Left
	']' : ("GREY", "BLACK"),				#Entrance Right
	'W' : ("APPOC_SKY", "APPOC_DEEP"),		#Water
	'w' : ("APPOC_SKY", "APPOC_SHALLOW"), 	#Reef
	'M' : ("APPOC_MOUNTAIN", "APPOC_SKY"),	#Mountain
	'm' : ("APPOC_MOUNTAIN", "APPOC_SKY"),	#Hill
	"X" : ("BROWN", "APPOC_GROUND"),		#Cliff
	"x" : ("DAY_ICE", "APPIC_GROUND"),		#Ice
	"#" : ("SUNSETPINK", "BLACK"),			#Hash wall
	"$" : ("GOLD", "BLACK"),				#Cash
	"L" : ("BLACK", "GOLD"),				#Next Level
	"l" : ("BLACK", "GOLD"),				#Previous Level
	"T" : ("APPOC_TREE", "APPOC_SKY"),		#Large Tree
	"t" : ("APPOC_TREE", "APPOC_GROUND"),	#Small Tree
	"F" : ("APPOC_TREE", "APPOC_SKY"),  	#Forest
	"_" : ("GREY", "APPOC_SKY"),			#Snow
	" " : ("WHITE", "APPOC_GRASS"),			#Field
	"d" : ("GREY", "BLACK"),				#Door
	"I" : ("BLACK", "BROWN"),				#Building Wall
	'=' : ("GREY", "DAY_GROUND"),			#Roof
	"S" : ("GOLD", "GOLD")					#Start
	}
	return lookup.get(char, ("RED", "BLACK"))