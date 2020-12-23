from sys import argv
import pygame.event
from lib.GameInstance import *


def main():
 
    kwargs = {}
    kwargs["map"]               = "world"
    kwargs["theme"]             = "text"
    kwargs["char_name"]     = "cat"
    kwargs["edit"]              = "no-edit"
    kwargs["player_name"]   = "CatJones"
    kwargs["load"]              = "yes"
    kwargs["round_world"]   = True
    kwargs["display_type"]  = "text"
    
    for i in range(len(argv)):
        if      argv[i][:4]     == "map="               :   kwargs["map"]               = argv[i][4:]
        elif    argv[i][:6]     == "theme="         :   kwargs["theme"]             = argv[i][6:]
        elif    argv[i][:10]        == "char_name=" :   kwargs["char_name"]     = argv[i][10:]
        elif    argv[i][:5]     == "edit="              :   kwargs["edit"]              = argv[i][5:]
        elif    argv[i][:12]        == "player_name="   :   kwargs["player_name"]   = argv[i][12:]
        elif    argv[i][:5]     == "load="              :   kwargs["load"]              = argv[i][5:]
        elif    argv[i][:12]        == "round_world="   :   kwargs["round_world"]   = argv[i][12:]
        elif    argv[i][:7]     == "-sprite"                :   kwargs["display_type"]  = "sprite"
        elif    argv[i]             == "-e"                 :   kwargs["edit"]                  = "edit"
        

        
    print("Usage: text.py [map={}] [theme={}] [character={}] [edit={}] [load={}][display_type={}]".format(
        kwargs["map"],
        kwargs["theme"],
        kwargs["char_name"],
        kwargs["edit"],
        kwargs["player_name"],
        kwargs["load"],
        kwargs["round_world"],
        kwargs["display_type"]
    ))
    
        
    game = GameInstance(**kwargs)
    game.next_frame()

    p_up    = False
    p_down  = False
    p_left  = False
    p_right = False
    
    ignore_movement = False
    
    #Main Loop
    while game.is_executing():
        #if game.new_view: game.update_current_view()
        game.next_frame()
        for event in pygame.event.get():
            extra_keys = pygame.key.get_mods()
            if event.type == pygame.QUIT:                                                           #Conclude execution if player quits             
                game.quit()     
            elif event.type == pygame.KEYDOWN:  
                if game.get_char() == 'x' and not game.can_walk() and not game.is_edit: ignore_movement = True
                else:                       ignore_movement = False
                if (    extra_keys & pygame.KMOD_CTRL 
                        and event.key == pygame.K_s):       game.save()                             #Press CTRL + S to save the current map
                elif (  extra_keys & pygame.KMOD_CTRL 
                        and event.key == pygame.K_a ):      game.save("ALL")                        #Press CTRL + A to save all maps
                elif (  extra_keys & pygame.KMOD_CTRL 
                        and event.key == pygame.K_q):       game.quit()                             #Press CTRL + Q to quit the game
                elif (  extra_keys & pygame.KMOD_CTRL
                        and event.key == pygame.K_g):       game.create_blank_layers()              #Press CTRL + G to generate maps for all layers
                elif game.can_edit() and game.is_edit() and event.key in range(pygame.K_SPACE, pygame.K_z+1):
                    if extra_keys & pygame.KMOD_SHIFT:      game.set_edit_char(event.key, True)     #Press SHIFT + key to draw it at the player's location
                                                
                    else:                                   game.set_edit_char(event.key, False)    #Press any key to draw it at the player's location
                        
                else:
                    if not ignore_movement: 
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:                       # < to move player left
                            if extra_keys & pygame.KMOD_CAPS:                   game.move_player("LEFT")
                            else:                                               p_left  = True                                                                      
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:                    # > to move player right
                            if extra_keys & pygame.KMOD_CAPS:                   game.move_player("RIGHT")
                            else:                                               p_right = True  
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:                       # ^ to move player up
                            if extra_keys & pygame.KMOD_CAPS:                   game.move_player("UP")
                            else:                                               p_up    = True                      
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:                     # v to move player down
                            if extra_keys & pygame.KMOD_CAPS:                   game.move_player("DOWN")
                            else:                                               p_down  = True  
                                
                    if event.key == pygame.K_1:
                        game.change_layer(MAP_LAYERS[0])                                                        #Press 0 for default zoom level
                    elif event.key == pygame.K_2:
                        game.change_layer(MAP_LAYERS[1])                                                            #Press 1 to increase zoom level
                    elif event.key == pygame.K_3:
                        game.change_layer(MAP_LAYERS[2])
                    elif event.key == pygame.K_4:
                        game.change_layer(MAP_LAYERS[3])                                                            #Press 3 to maximize 
                    elif event.key == pygame.K_5:
                        game.change_layer(MAP_LAYERS[4])
                    elif event.key == pygame.K_6:
                        game.change_layer(MAP_LAYERS[5])
                    
                    elif event.key == pygame.K_EQUALS:
                        game.modify_zoom(1)
                    elif event.key == pygame.K_MINUS:
                        game.modify_zoom(-1)
                        
                    elif event.key == pygame.K_SPACE:                                               #Press space for ACTION
                            game.take_action()
            
                    elif event.key == pygame.K_F1:
                        game.toggle_collision()                                                     #Press F1 to toggle collision
                        
                    elif event.key == pygame.K_PAGEUP:
                        game.change_player_move_speed(-10)                                          #Press PAGEUP to increase movement speed
                        
                    elif event.key == pygame.K_PAGEDOWN:
                        game.change_player_move_speed(10)                                           #Press PAGEDOWN to decrease movement speed
                    
                    elif event.key == pygame.K_F2 and game.can_edit():
                        game.toggle_editmode()                                                      #Press F2 to toggle edit mode
                    
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT       or event.key == pygame.K_a:     p_left = False
                elif event.key == pygame.K_RIGHT    or event.key == pygame.K_d:     p_right = False
                elif event.key == pygame.K_UP       or event.key == pygame.K_w:     p_up = False
                elif event.key == pygame.K_DOWN     or event.key == pygame.K_s:     p_down = False
                
        game.process_movement(p_up, p_down, p_left, p_right)

if __name__=="__main__":
    main()
    
    
