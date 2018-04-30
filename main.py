# Imports
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import numpy as np
import cv2
import math
import sys, pygame
import os
import itertools
from itertools import combinations
import random
from random import randint
import logging

import lib.images as images
import lib.generate as generate
import lib.calibrate as calibrate
import lib.camera as cam
import lib.conversions as conversions
import lib.classes as classes
import lib.players_ships_planets_classes as psp_classes

IMAGE_CAPTURE_DELAY = 1
SHIP_SCAN_SIZE = 8
ISO_VALUE = 400
SCAN_BRIGHTNESS = 150
CALIBRATE_COLOUR_LOCATIONS = True
CALIBRATE_COLOURS = True
SCAN_SHIP_COLOURS = True
CALIBRATE_CONTROL_DOTS = True
CALIBRATE_CONTROL_DOTS_TEST = False
CALIBRATE_HEX_DOTS_SLOW = False
CALIBRATE_HEX_DOTS_FAST = True



# set up logging
#logging.basicConfig(filename = os.path.join("logs", "gamelog.log"), level = logging.DEBUG)
logging.basicConfig(filename = os.path.join("logs", "gamelog.log"), level = logging.INFO)
logging.info('--------COMMENCING--------')
logging.info('--------COMMENCING--------')
logging.info('--------COMMENCING--------')


# Take-in User Arguments
if len(sys.argv)==2:
    BOARD_SIZE = int(sys.argv[1])
else:
    BOARD_SIZE = 3 # there will be 3*2+1 = 7 tiles, vertically

#Set board dimensions
#for projector:
SIZE = WIDTH, HEIGHT = 1150,550
#SIZE = WIDTH, HEIGHT = 1650,900
#for kyle's tv
#size = width, height = 1200,900
CONTROL_BOARD_WIDTH = int(WIDTH/4.4)

# Initialize Gameboard
GameBoard = classes.Zones(5, WIDTH, HEIGHT, CONTROL_BOARD_WIDTH, BOARD_SIZE)
logging.info('GameBoard generated')

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((GameBoard.width,GameBoard.height))


# shows you what the camera's view is and lets you readjust before moving on with program
cam.capture_image('whatCameraSees.jpg')
inpu = input('Are you ready to begin calibration?')
while 1:
    if inpu == 'n' or inpu == 'N':
        cam.capture_image('whatCameraSees.jpg')
        inpu = input('Howabout now...?')
    else:
        break


#-------------------------------------------------------------#
#CALIBRATE GAMEBOARD COLOUR DOT CALIBRATION LOCATIONS & COLOURS
#-------------------------------------------------------------#
if CALIBRATE_COLOUR_LOCATIONS:
    calibrate.calibrate_gameboard_dots(GameBoard, screen, pygame.display.flip, cam.capture_image,  test_ind = 0)

if CALIBRATE_COLOURS:
    GameBoard.average_hsv_calibration(screen, pygame.display.flip, cam, cv2, 4, ISO_VALUE, SCAN_BRIGHTNESS, IMAGE_CAPTURE_DELAY)
    GameBoard.mask_loc_names = cam.capture_hsv_ranges("ScanMasterImage.jpg", GameBoard.colour_thresholds, ISO_VALUE, screen, SCAN_BRIGHTNESS, pygame.display.flip, IMAGE_CAPTURE_DELAY, kernel_size = 3)
logging.info('GameBoard colours located and calibrated')
    
#-------------------------------------------------------------#
#CREATE & CALIBRATE CONTROL DOTS WITH CAMERA
#-------------------------------------------------------------#

ControlBoards = classes.ControlBoards

control_boards_list = []    
for x in GameBoard.control_board_dimensions_list:
    control_boards_list.append(ControlBoards(x))
logging.info('ControlBoards generated')

if CALIBRATE_CONTROL_DOTS:
    calibrate.calibrate_control_dots(ControlBoards, screen, pygame.display.flip, cam.capture_image, 0)
elif CALIBRATE_CONTROL_DOTS_TEST:
    calibrate.calibrate_control_dots(ControlBoards, screen, pygame.display.flip, cam.capture_image, 1)

#logging.info('Control dot calibration complete')
    #return x, y

#-------------------------------------------------------------#



#-------------------------------------------------------------#
#CREATE ALL HEX OBJECTS
#-------------------------------------------------------------#

# Define and Initialize the HexTiles class
HexTiles = classes.HexTiles
HexTiles.initialize_class_params(GameBoard)

#calculate all zone coordinates in cubic coordinates : zone_list_hex
zone_list_hex = generate.cubic_hex(GameBoard.board_size)

#sort that list of hexes
zone_list_hex_sorted = generate.sorted_zones(GameBoard.num_columns, GameBoard.board_size, zone_list_hex)

hexesBigList = []
for i in range(len(zone_list_hex_sorted)):
    hexesBigList.append(HexTiles(zone_list_hex_sorted[i][0:3], conversions, GameBoard))
logging.info('HexTiles Generated')

#add neighbours to each hex
for hex in HexTiles.instances_list:
    hex.initialize_neighbour_objects(GameBoard, HexTiles)
logging.info('Neighbours assigned for each Hex Tile')
#-------------------------------------------------------------#


#-------------------------------------------------------------#
#CALIBRATE HEX SHIP DETECT VERTS WITH CAMERA
#-------------------------------------------------------------#
if CALIBRATE_HEX_DOTS_SLOW:
    calibrate.calibrate_hex_dots_slow(GameBoard, HexTiles, screen, pygame.display.flip, cam.capture_image)

if CALIBRATE_HEX_DOTS_FAST:
    calibrate.calibrate_hex_dots_fast(GameBoard, HexTiles, screen, pygame.display.flip, cam.capture_image)
#-------------------------------------------------------------#




#-------------------------------------------------------------#
#CREATE ALL PLAYER OBJECTS
#-------------------------------------------------------------#
Players = psp_classes.Players
player_list = []
for i in range(4):
    player_list.append(Players(i + 1, ControlBoards.instances_list[i], images.planet_image_list[i], images.ship_image_list[i]))
logging.info('Players created')

# set each control board player_object to relevant player
for player in Players.instances_list:
    player.control_board_object.player_object = player
#-------------------------------------------------------------#


#-------------------------------------------------------------#
#DEFINE SHIPS CLASS
#-------------------------------------------------------------#
Ships = psp_classes.Ships
#-------------------------------------------------------------#


#-------------------------------------------------------------#
#CREATE ALL PLANET OBJECTS
#-------------------------------------------------------------#
Planets = psp_classes.Planets
planets_list = []
starters , unclaimed = generate.generate_planet_placements(GameBoard.board_size, config = 1)
for counter, player in enumerate(Players.instances_list):
    player.planets_list.append(Planets(player.planet_image, starters[counter], HexTiles, GameBoard, conversions, player))
for player in Players.instances_list:
    for planet in player.planets_list:
        planet.hex_object.visible = 1
for uncl in unclaimed:
    planets_list.append(Planets(images.planet_image_list[8], uncl, HexTiles, GameBoard, conversions, None))
logging.info('Planets created')
#-------------------------------------------------------------#


#-------------------------------------------------------------#
#CREATE ALL TECHNOLOGY OBJECTS
#-------------------------------------------------------------#
Techs = psp_classes.Techs
for player in Players.instances_list:
    player.tech_object = Techs(player, HexTiles)
#-------------------------------------------------------------#

PlasmaStorms = psp_classes.PlasmaStorms
plasma_storm_list = []





#-------------------------------------------------------------#
#SCRIPT TO DRAW/refresh BOARD
#-------------------------------------------------------------#
def paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms):
    screen.blit(bgb, (0,0))        

    for x in Planets.instances_list:
        x.draw_planet(screen)
        
    for x in HexTiles.instances_list:
        x.drawmelikeoneofyourfrenchgirls(screen, i)
        x.drawDots(screen, i, 2)
    
    for x in Players.instances_list:
        x.control_board_object.draw_control_dots(screen, i, 6)
        x.control_board_object.print_allies(screen)
        #if it's your turn print the playet title as white, otherwise a diff colour
        if x.player_num == playerTurnInd:
            x.control_board_object.print_title(screen, x.player_num, x.sci_resource, x.prd_resource, (255,255,255))
            x.tech_object.draw_random_tech(screen, x.control_board_object.control_dot_locations)
        else:
            x.control_board_object.print_title(screen, x.player_num, x.sci_resource, x.prd_resource, (255,100,20))

    for ship in Ships.instances_list:
        ship.draw_ship(screen)
        
    #draw plasma storms
    if PlasmaStorms.instances_list:
        for storm in PlasmaStorms.instances_list:
            storm.draw_storm(screen)


#-------------------------------------------------------------#
#SETUP INITIAL BOARD CONDITIONS
#-------------------------------------------------------------#
bgb = pygame.transform.scale(pygame.image.load(os.path.join("images", "board", images.background_image)),(GameBoard.width,GameBoard.height))

#play game initiation sound
pygame.mixer.init()
pygame.mixer.set_num_channels(1)
#sound = pygame.mixer.Channel(1)
#soundfile = pygame.mixer.Sound(os.path.join("audio", "initializeGame.mp3"))
#sound.play(soundfile)
pygame.mixer.music.load(os.path.join("audio", "initializeGame.mp3"))
pygame.mixer.music.play()

playerTurnInd = randint(1,4)
print("player turn ind: " + str(playerTurnInd))
plasma_storm_list = []
scanner_ship_id_xy_list = []
plasma_storms_list = []
colorDirxn=1
i=1
turnCounter = 1
#who is the current player
for player in Players.instances_list:
    if player.player_num == playerTurnInd:
        currPlayer = player
logging.info('..drawing random tech for next player')
currPlayer.grab_random_tech()
currPlayer.harvest_resources()
#-------------------------------------------------------------#




#-------------------------------------------------------------#
#RUN RUN RUN RUN RUN RUN RUN RUN RUN RUNHUN RUN RUN RUN RUN
#-------------------------------------------------------------#
while 1:

    #CHECK FOR SCREEN CLOSURE
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    #HANDLE KEY PRESSES
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]: sys.exit()
        
    #MAKE ALL INVIXIBLE HEX TILES VISIBLE. PRESSING A SECOND TIME TO UNDO. USED FOR DEMO PURPOSES
    if pressed_keys[pygame.K_SPACE]:
        logging.info('<spacebar pressed> Changing HexTiles between visible/invisible')
        for x in HexTiles.instances_list:
            if x.visible == 0:
                x.visible = 2
            elif x.visible == 2:
                x.visible = 0
        time.sleep(.2)
        
    #RECALIBRATE COLOUR THRESHOLDING RANGES
    if pressed_keys[pygame.K_c]:
        logging.info("<key 'c' pressed> Recalibrating colours")
        #display a number of dots equal to n_colours
        GameBoard.average_hsv_calibration(screen, pygame.display.flip, cam, cv2, 4, ISO_VALUE, SCAN_BRIGHTNESS, IMAGE_CAPTURE_DELAY)
        logging.debug('Average Hues detected: %s', GameBoard.average_hsv_list)
        GameBoard.mask_loc_names = cam.capture_hsv_ranges("ScanMasterImage.jpg", GameBoard.colour_thresholds, ISO_VALUE, screen, SCAN_BRIGHTNESS, pygame.display.flip, IMAGE_CAPTURE_DELAY, kernel_size = 3)
        #setColourThresholds()
        time.sleep(.2)
        
    #END CURRENT PLAYERS TURN AND PROCESS ALL MOVES
    if pressed_keys[pygame.K_RETURN]:
        
        logging.info('<return key pressed> Processing Turn #' + str(turnCounter))
        logging.info('..updating players list of owned ships')
        for player in Players.instances_list:
            player.ships_list = []
            for ship in Ships.instances_list:
                if ship.player_object.player_num == player.player_num:
                    player.ships_list.append(ship)

        
        #downgrade current plasma storms
        if PlasmaStorms.instances_list:
            for storm in PlasmaStorms.instances_list:
                storm.downgrade_storm()
        #randomly generate a plasma storm
        plasma_storms_list.append(PlasmaStorms.randomly_generate_storms(HexTiles, turnCounter))

        logging.info('..scanning board colours')
        GameBoard.mask_loc_names = cam.capture_hsv_ranges("ScanMasterImage.jpg", GameBoard.colour_thresholds, ISO_VALUE, screen, SCAN_BRIGHTNESS, pygame.display.flip, IMAGE_CAPTURE_DELAY, kernel_size = 3)
        logging.debug('mask_loc_names: %s', GameBoard.mask_loc_names)
        loaded_mask_list = [cv2.imread(img, 0) for img in GameBoard.mask_loc_names]
        
        logging.info('..applying ship movements for current player')
        scanner_ship_id_xy_list = []
        for hex in HexTiles.instances_list:
            ship_ids , ship_vertices , ship_hex_objects = hex.detect_ships(GameBoard, loaded_mask_list, logging, scansize = SHIP_SCAN_SIZE)
            if ship_ids:
                for j in range(len(ship_ids)):
                    if currPlayer.ships_list:
                        for playership in currPlayer.ships_list:
                            #if there's a ship detected and it belongs to the current player then update it's position
                            if playership.ship_id == ship_ids[j]:
                                playership.hex_vertice = ship_vertices[j]
                                playership.hex_object = ship_hex_objects[j]
        
        paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
        pygame.display.flip()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        
        logging.info('..constructing new ships in orbit for current player')
        # find ships orbiting current player's planets
        for planet in currPlayer.planets_list:
            ship_ids , ship_vertices , ship_hex_objects = planet.hex_object.detect_ships(GameBoard, loaded_mask_list, logging, scansize = SHIP_SCAN_SIZE)
            # if ship doesn't exist then create it
            if ship_ids:
                for j in range(len(ship_ids)):
                    if ship_ids[j] not in Ships.instances_id_list:
                        currPlayer.ships_list.append(Ships(currPlayer.ship_image, ship_ids[j], ship_vertices[j], ship_hex_objects[j], HexTiles, conversions, currPlayer))
                        currPlayer.sci_resource -= Ships.sci_cost
                        currPlayer.prd_resource -= Ships.prd_cost
                        pygame.mixer.music.load(os.path.join("audio", "launchShip.mp3"))
                        pygame.mixer.music.play()
        
        logging.info('..reading control board for current player')
        control_selections = currPlayer.control_board_object.read_control_dots(loaded_mask_list, logging, scansize = 8)
        logging.debug('Control dots detected: %s', control_selections)
        print('Control Board for player %s registered as:', currPlayer.player_num)
        print(control_selections)
        paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
        pygame.display.flip()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        
        logging.info('..processing control board for current player')
        # tech purchases
        for j in range(3):
            if control_selections[j] == 1:
                currPlayer.tech_object.purchase_tech(j)
                #pygame.mixer.music.load(os.path.join("audio", "buyTech3.wav"))
                #pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        # alliances list
        currPlayer.alliances_list = []
        for j in range(1,4):
            if control_selections[j+2] == 1:
                if j < currPlayer.player_num:
                    currPlayer.alliances_list.append(j)
                else:
                    currPlayer.alliances_list.append(j+1)
        if currPlayer.alliances_list:
            print('player aliances %s ' , currPlayer.alliances_list)
            pygame.mixer.music.load(os.path.join("audio", "activateAlliance.wav"))
            pygame.mixer.music.play()
            
        paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
        pygame.display.flip()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        
        logging.info('..regenerating health bars')
        for ship in Ships.instances_list:
            ship.regenerate_health()
            ship.scan_area()
        for planet in Planets.instances_list:
            planet.regenerate_health()
            
        logging.info('..processing combat')
        if Ships.instances_list:
            for ship in Ships.instances_list:
                ship.shoot_enemy_ships(Ships)
                ship.shoot_enemy_planets(Planets)
            for planet in Planets.instances_list:
                ship.shoot_enemy_ships(Ships)
            paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
            pygame.display.flip()
            while pygame.mixer.music.get_busy():
                time.sleep(0.01)
            
            # ships capture planets. Where there is conflict, more experienced ships get the planet (based on creation order)
            for ship in reversed(Ships.instances_list):
                ship.capture_enemy_planets(Planets)
            #refresh list of planets owned by each player
            for player in Players.instances_list:
                player.planets_list = []
                for planet in Planets.instances_list:
                    if planet.player_object is not None:
                        if planet.player_object.player_num == player.player_num:
                            player.planets_list.append(planet)
                logging.info("Player " + str(player.player_num) + " currently owns " + str(len(player.planets_list)) + " planets")
        
        paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
        pygame.display.flip()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        
        #process storm damage to ships
        logging.info('..plasma storms doing damage')
        if PlasmaStorms.instances_list:
            for storm in PlasmaStorms.instances_list:
                storm.damage_enemy_ships(Ships)
        
        #delete destroyed ships
        logging.info('..destroying dead ships')
        if Ships.instances_list:
            for ship in Ships.instances_list:
                ship.delete_destroyed()
        
        paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
        pygame.display.flip()
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
        
        logging.info('..updating player turn indicator')
        turnCounter += 1
        playerTurnInd += 1
        if playerTurnInd > 4:
            playerTurnInd = 1
        #who is the new current player
        for player in Players.instances_list:
            if player.player_num == playerTurnInd:
                currPlayer = player
        logging.info('..drawing random tech for next player')
        currPlayer.grab_random_tech()
        currPlayer.harvest_resources()
    
    
    
    #REPAINT BOARD REPEATEDLY
    paint_board(screen,bgb,i,playerTurnInd,Planets,HexTiles,Players,Ships,PlasmaStorms)
    
    """
    screen.blit(bgb, (0,0))        

    for x in Planets.instances_list:
        x.draw_planet(screen)
        
    for x in HexTiles.instances_list:
        x.drawmelikeoneofyourfrenchgirls(screen, i)
        x.drawDots(screen, i, 2)
    
    for x in Players.instances_list:
        x.control_board_object.draw_control_dots(screen, i, 6)
        x.control_board_object.print_allies(screen)
        #if it's your turn print the playet title as white, otherwise a diff colour
        if x.player_num == playerTurnInd:
            x.control_board_object.print_title(screen, x.player_num, x.sci_resource, x.prd_resource, (255,255,255))
            x.tech_object.draw_random_tech(screen, x.control_board_object.control_dot_locations)
        else:
            x.control_board_object.print_title(screen, x.player_num, x.sci_resource, x.prd_resource, (255,100,20))

    for ship in Ships.instances_list:
        ship.draw_ship(screen)
        
    #draw plasma storms
    if PlasmaStorms.instances_list:
        for storm in PlasmaStorms.instances_list:
            storm.draw_storm(screen)
    """
    #MAKE HEXGRID PHASE IN AND OUT
    i+=7*colorDirxn
    if i>255:
        i=255
        colorDirxn=-1
    if i<1:
        i=0
        colorDirxn=1
    pygame.display.flip()
    time.sleep(.05)

#-------------------------------------------------------------#
