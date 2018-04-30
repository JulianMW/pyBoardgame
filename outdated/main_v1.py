# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import sys, pygame
from modules4 import *
import csv
import math
from PIL import Image
import os
import itertools
from itertools import combinations
import random
from random import randint
#import argparse



# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1) # allow the camera to warmup

#initialize pygame
pygame.init()
global size, width, height, black, BOARD_CENTER, BOARD_COLUMNS, hex_edge_dist, hex_side_length



global hsvrng1a, hsvrng1ax, hsvrng2a, hsvrng3a, hsvrng4a, hsvrng5a, hsvrng6a
global hsvrng1b, hsvrng1bx, hsvrng2b, hsvrng3b, hsvrng4b, hsvrng5b, hsvrng6b
global hsv1frame, hsv2frame, hsv3frame, hsv4frame, hsv5frame, hsv6frame

dftl = 27
saturtna = 60
vallua = 60
saturtnb = 255
vallub = 155
# DEFINE colour thresholds
hsvrng1a = np.array([0*179/360,saturtna,vallua])
hsvrng1ax = np.array([340*179/360,saturtna,vallua])
hsvrng2a = np.array([(60-dftl)*179/360,saturtna,vallua])
hsvrng3a = np.array([(120-dftl)*179/360,saturtna,vallua])
hsvrng4a = np.array([(180-dftl)*179/360,saturtna,vallua])
hsvrng5a = np.array([(240-dftl)*179/360,saturtna,vallua])
hsvrng6a = np.array([(290-dftl)*179/360,saturtna,vallua])

hsvrng1b = np.array([(dftl)*179/360,saturtnb,vallub])
hsvrng1bx = np.array([(359.9)*179/360,saturtnb,vallub])
hsvrng2b = np.array([(60+dftl)*179/360,saturtnb,vallub+20])
hsvrng3b = np.array([(120+dftl)*179/360,saturtnb,vallub])
hsvrng4b = np.array([(180+dftl)*179/360,saturtnb,vallub])
hsvrng5b = np.array([(240+dftl)*179/360,saturtnb,vallub])
hsvrng6b = np.array([(300+dftl)*179/360,saturtnb,vallub])

def setColourThresholds():
    dftl = 20
    sat_dftl = 20
    val_dftl = 20

    if ControlBoard.control_boards_list[0].col_hues[0] < dftl:
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([( 360 - dftl + ControlBoard.control_boards_list[0].col_hues[0])*180/360  ,  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  360  )*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    elif ControlBoard.control_boards_list[0].col_hues[0] > (360 - dftl):
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0] - dftl)*180/360  ,  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  dftl - (360 -  ControlBoard.control_boards_list[0].col_hues[0])  )*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),  int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    else:
        hsvrng1a = np.array([(ControlBoard.control_boards_list[0].col_hues[0]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0] + dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1bx = np.array([(ControlBoard.control_boards_list[0].col_hues[0] + dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        
                            
        

    #hsvrng1a =  np.array([  0,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    #hsvrng1ax = np.array([340*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    
    hsvrng2a = np.array([(ControlBoard.control_boards_list[0].col_hues[1]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    hsvrng3a = np.array([(ControlBoard.control_boards_list[0].col_hues[2]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[2]/2),int(ControlBoard.control_boards_list[0].col_vals[2]/2)])
    hsvrng4a = np.array([(ControlBoard.control_boards_list[0].col_hues[3]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[3]/2),int(ControlBoard.control_boards_list[0].col_vals[3]/2)])
    hsvrng5a = np.array([(ControlBoard.control_boards_list[0].col_hues[4]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[4]/2),int(ControlBoard.control_boards_list[0].col_vals[4]/2)])
    hsvrng6a = np.array([(ControlBoard.control_boards_list[0].col_hues[5]-dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[5]/2),int(ControlBoard.control_boards_list[0].col_vals[5]/2)])

    #hsvrng1b =  np.array([(dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    #hsvrng1bx = np.array([(359.9)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    
    hsvrng2b = np.array([(ControlBoard.control_boards_list[0].col_hues[1]+dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    hsvrng3b = np.array([(ControlBoard.control_boards_list[0].col_hues[2]+dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[2]+20),int(ControlBoard.control_boards_list[0].col_vals[2]+20)])
    hsvrng4b = np.array([(ControlBoard.control_boards_list[0].col_hues[3]+dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[3]+20),int(ControlBoard.control_boards_list[0].col_vals[3]+20)])
    hsvrng5b = np.array([(ControlBoard.control_boards_list[0].col_hues[4]+dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[4]+20),int(ControlBoard.control_boards_list[0].col_vals[4]+20)])
    hsvrng6b = np.array([(ControlBoard.control_boards_list[0].col_hues[5]+dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[5]+20),int(ControlBoard.control_boards_list[0].col_vals[5]+20)])


global SHIP_SEARCH_SIZE 
SHIP_SEARCH_SIZE = 5 #the size of the area to search for ship pixels (in pixels)

#for projector:
size = width, height = 1150,550
#for kyle's tv
#size = width, height = 1200,900
bufferSize = 0 #how much blank space you want around the outside
leftRightBuffer = 200
#leftRightBuffer = 180
black = 0, 0, 0
screen = pygame.display.set_mode(size)
global CTRL_DOT_DIST, N_CTRL_DOTS, TECH_SIZE, PLASMA_STORM_SIZE
N_CTRL_DOTS = 6
CTRL_DOT_DIST= height/(N_CTRL_DOTS*2 + 2)
TECH_SIZE = int(height/18) 
PLASMA_STORM_SIZE = int(height/25) 

#SET INITIAL VARIABLES TO SELECTION OR DEFAULT
if len(sys.argv)>1:
    BOARD_SIZE = int(sys.argv[1])
    NPLAYERS = int(sys.argv[2])
else:
    BOARD_SIZE = 3
    NPLAYERS = 4
BOARD_CENTER = [width/2,height/2]
BOARD_COLUMNS = BOARD_SIZE * 2 + 1
board_columns_rows = []
NTOTAL_HEXES=0




#load the backgroud image to be painted on every iteration
#bgb = pygame.image.load(os.path.join("Images", "pyBoardgameBackgroundx2.jpg"))
bgb = pygame.transform.scale(pygame.image.load(os.path.join("Images", "pyBoardgameBackgroundx4.jpg")),(width,height))

for i in range(1,BOARD_COLUMNS + 1):
    if i <= BOARD_SIZE +1:
        board_columns_rows.append(BOARD_SIZE+i)
    elif i>BOARD_SIZE +1:
        board_columns_rows.append(BOARD_SIZE*2 - (i-BOARD_SIZE-2))
    NTOTAL_HEXES += board_columns_rows[i-1]

print('board_columns_rows:' ,board_columns_rows)
print('NTOTAL_HEXES:' ,NTOTAL_HEXES)

    
shipfont = pygame.font.SysFont("monospace", 12)
controlfont = pygame.font.SysFont("monospace", 16)

#defines the distance to the flat part of the hex
#allows one hex-sized buffer on each side of board
hex_edge_dist = min(width-bufferSize*2, width - leftRightBuffer*2, height-bufferSize*2) / (BOARD_SIZE*4 +3)

hex_side_length= hex_edge_dist / (math.cos(math.radians(30)))

print("edge distance: ",hex_edge_dist)
print("side lentgh: ",hex_side_length)

zone_list_hex = []
zone_pixels_cart = []



#generate ship identifiers - 6 hues w/ 4colour die
def generateShipId():
    in_list = [0, 1, 2, 3, 4, 5]
    out_list = []
    for i in range(1, 5):
        out_list.extend(itertools.combinations(in_list, i))    


    out_list2 = []
    for i in out_list:
        inter_list = [0,0,0,0,0,0]
        for j in range(0,6):
            if j in i:
                inter_list[j] = 1
        out_list2.append(inter_list)
    return out_list2

shipIds = generateShipId();
print(shipIds)




#4players
#playernum, starting planet loc
LocPlayer = [[-BOARD_SIZE,0,BOARD_SIZE,1],[-BOARD_SIZE,BOARD_SIZE,0,2],[BOARD_SIZE,-BOARD_SIZE,0,3],[BOARD_SIZE,0,-BOARD_SIZE,4]]
extraPlanets = [[0,0,0,0], [1,-1,0,0]]


#list of hex coords with starting planets
#order: <playerIdentifier>,x,y,z .... 0==center
#2 players:
#planetHexList = [[-3,3,0],[3,-3,0]]
#3 players:
#planetHexList = [[-3,3,0],[0,-3,3],[3,0,-3]]
#4 players:
#planetHexList = [[-3,3,0,1],[-3,0,3,2],[3,-3,0,3],[3,0,-3,4],[0,0,0,0]]
planet_image_list = ["p_normal.png","p1shaded.png","p2shaded.png","p3shaded.png","p4shaded.png","p5shaded.png","p6shaded.png"]


#shipHexList = [[-2,2,0,1],[-2,0,2,2],[2,-2,0,3],[2,0,-2,4],[0,0,0,0]]
ship_image_list = ["ship7.png","ship1.png","ship2.png","ship3.png","ship4.png","ship5.png","ship6.png"]
global ship_size
ship_size = [int(hex_side_length*2/6),int(hex_side_length*4/6)]







#FUNCTION DEFINITIONS
def cubiToCart(xxyyzz):
    x = xxyyzz[0]  * (3/2) * hex_side_length + width/2
    y = math.sqrt(3) * hex_side_length * (xxyyzz[0]/2 + xxyyzz[1]) + height/2
    return x, y

neighbours_list = [[1,-1,0],[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1]]
def findNeighbours(xxyyzz):
    nbrs = []
    for x in range(len(neighbours_list)):
        a = [xxyyzz[i] + neighbours_list[x][i] for i in range(len(xxyyzz))]
        if a in zone_list_hex:
            nbrs.append(a)
    return nbrs


#HSL Detection - given an image array in hsv itwill output the identity of any shi p theredetected
#for opencv hsv hue range is [-,179], sat and val range is [0,255]
hue = 0
hue = hue/360*179





def findShipId(hsvImageArray,xy,size):
    out_array = [0,0,0,0,0,0]
    pixel_sum = [0,0,0,0,0,0] #keeps track of the count of each hue-matching pixel
    for i in range(0,5):
        ROI = hsvImageArray[i][int(xy[0]-size):int(xy[0]+size), int(xy[1]-size):int(xy[1]+size)]
        numPixels = len(ROI)
        print("LEN ROI = ", numPixels)
        print("ROI = ", ROI)
        for pixx in ROI:
            if( pixx[2]> 200 ):
                pixel_sum[i] += 1
        if pixel_sum[i] > numPixels/20:
            out_array[i] = 1
            
    #if out_array != [0,0,0,0,0,0]:
        #print("[SUCCESS] motherfucking shipid ", out_array)
    return out_array



def processShipMoves():

    
    pygame.mixer.music.load(os.path.join("Sounds", "appear.mp3"))
    pygame.mixer.music.play()
    
    #draw black
    screen.fill(black)
    #draw bright ship dots
    for x in hexesBigList:
        x.drawCalibrationDots(1,22)
        x.drawCalibrationDots(2,22)
        x.drawCalibrationDots(3,22)
    
    pygame.display.flip()
    camera.capture('shipMasterImage.jpg')
    shipsImg = cv2.imread('shipMasterImage.jpg')
    hsv_shipsImg = cv2.cvtColor(shipsImg, cv2.COLOR_BGR2HSV)
    #print(hsv_shipsImg)

    global hsv_frames_list

    #create a colour frame & image for each colour in detection
    # ranges defined at top of program
    hsv1framea = cv2.inRange(hsv_shipsImg,hsvrng1a,hsvrng1b)
    hsv1frameb = cv2.inRange(hsv_shipsImg,hsvrng1ax,hsvrng1bx)
    hsv1frame = cv2.add(hsv1framea,hsv1frameb)
    hsv2frame = cv2.inRange(hsv_shipsImg,hsvrng2a,hsvrng2b)
    hsv3frame = cv2.inRange(hsv_shipsImg,hsvrng3a,hsvrng3b)
    hsv4frame = cv2.inRange(hsv_shipsImg,hsvrng4a,hsvrng4b)
    hsv5frame = cv2.inRange(hsv_shipsImg,hsvrng5a,hsvrng5b)
    hsv6frame = cv2.inRange(hsv_shipsImg,hsvrng6a,hsvrng6b)
    hsv_frames_list = []
    hsv_frames_list.append(hsv1frame)
    hsv_frames_list.append(hsv2frame)
    hsv_frames_list.append(hsv3frame)
    hsv_frames_list.append(hsv4frame)
    hsv_frames_list.append(hsv5frame)
    hsv_frames_list.append(hsv6frame)
    cv2.imwrite('frame1.jpg',hsv1frame)
    cv2.imwrite('frame2.jpg',hsv2frame)
    cv2.imwrite('frame3.jpg',hsv3frame)
    cv2.imwrite('frame4.jpg',hsv4frame)
    cv2.imwrite('frame5.jpg',hsv5frame)
    cv2.imwrite('frame6.jpg',hsv6frame)

    #loop over hex detection points and identify ships at each point
    #assign ship locations to ships as they are detected
    for xe in hexesBigList:
        xe.scanForShips(hsv_frames_list)
    for x in Ship.ships_list:
        x.updateLocation()
        x.updateHexObjectShipslist()

    #updateLocation()
    #updateHexObjectShipslist()



def deleteDestroyedShips():
    for ship in Ship.ships_list:
        if ship.Health <=0:
            ship.destroyShip()
            print("ShipDestroyed")
            pygame.mixer.music.load(os.path.join("Sounds", "powerup2.mp3"))
            pygame.mixer.music.play()
            time.sleep(0.1)




def processShipCombat():

    
    pygame.mixer.music.load(os.path.join("Sounds", "computer.mp3"))
    pygame.mixer.music.play()

    #loop over ships to find targets within range
    for sh in Ship.ships_list:
        sh.ship_targets = []
        
        #loop over enemy ships and add rel ones to targets
        for esh in Ship.ships_list:
            if ( (esh.playerObj != sh.playerObj) and (esh.playerObj.playerNo not in sh.playerObj.alliances_playerNos) and (sh.Range == 0) and (sh.HexObject == esh.HexObject) ):
                sh.ship_targets.append(esh)
            if ( (esh.playerObj != sh.playerObj) and (esh.playerObj.playerNo not in sh.playerObj.alliances_playerNos) and (sh.Range == 1) and (esh.HexObject.xxyyzz in findNeighbours(sh.xxyyzz)) ):
                sh.ship_targets.append(esh)

    for sh in Ship.ships_list:
        if sh.ship_targets != []:
            target = random.sample(sh.ship_targets,1)
            target[0].Health -= sh.Damage * randint(0,50)
                 
    #destroy ships with negative health
    deleteDestroyedShips()



def processPlanetCombat():

    
    pygame.mixer.music.load(os.path.join("Sounds", "computer.mp3"))
    pygame.mixer.music.play()
    
    #loop over planets and hexships
    for planet in Planet.planets_list:
        if planet.hexObject.ship_objects:
            for ship in planet.hexObject.ship_objects:
                if ship.playerNo != planet.playerNo:
                    ship.Health -= planet.Damage * randint(0,50)
                    planet.Health -= ship.Damage * randint(0,50)
                    
    #destroy ships with negative health
    deleteDestroyedShips()
    

def processLongRangeShipVsPlanetCombat():

    #loop over ships to find targets within range
    for sh in Ship.ships_list:
        sh.planet_targets = []
        
        #loop over enemy planets and add rel long-distance ones to targets
        for epl in Planet.planets_list:
            if ( (epl.owner) and (epl.owner.playerNo not in sh.playerObj.alliances_playerNos) and (sh.Range == 1) and (epl.hexObject.xxyyzz in findNeighbours(sh.xxyyzz)) ):
                sh.planet_targets.append(epl)

    for sh in Ship.ships_list:
        if sh.planet_targets != []:
            target = random.sample(sh.planet_targets,1)
            target[0].Health -= sh.Damage * randint(0,50)
                

def processPlanetCaptures():
    
    #increase ship health to max of 100
    for planet in Planet.planets_list:
        if planet.hexObject.players_present:
            #if planet shield is down and planet has no defending ships 
            if planet.Health<=0 and planet.hexObject.players_present.count(planet.playerNo) == 0:
                #and if there is a single enemy player present
                if len(list(set(planet.hexObject.players_present))) == 1:
                    planet.transferControl(planet.hexObject.players_present[0])


def shipSelfRepair():

    
    pygame.mixer.music.load(os.path.join("Sounds", "computer.mp3"))
    pygame.mixer.music.play()
    
    #increase ship health to max of 100
    for ship in Ship.ships_list:
        ship.Health = min(ship.Health + 10 * ship.Repair,ship.maxHealth)

def planetSelfRepair():
    
    #increase planet health to max of ship.maxHealth 
    for planet in Planet.planets_list:
        planet.Health = min(planet.Health + 10 * planet.Repair,planet.maxHealth )



def checkWinCondition(turnNum):
    p1wn = 0
    p2wn = 0
    p3wn = 0
    p4wn = 0

    if turnNum > 9:
        for ship in Ship.ships_list:
            if ship.playerObj.playerNo == 1:
                p1wn +=1
            elif ship.playerObj.playerNo == 2:
                p2wn +=1
            elif ship.playerObj.playerNo == 3:
                p3wn +=1
            elif ship.playerObj.playerNo == 4:
                p4wn +=1

        if p1wn > (p2wn+p3wn+p4wn)*1.5:
            return "Player One Wins"
        if p2wn > (p1wn+p3wn+p4wn)*1.5:
            return "Player Two Wins"
        if p3wn > (p2wn+p1wn+p4wn)*1.5:
            return "Player Three Wins"
        if p4wn > (p2wn+p3wn+p1wn)*1.5:
            return "Player Four Wins"
        else:
            return None
    else:
        return None



#calculate all zone coordinates in cubic coordinates : zone_list_hex
zone_list_hex = generateCubicHex(BOARD_SIZE)

#convert cubic coordinates to cartesian : zone_pixels_cart
zone_pixels_cart = generateCartHex(zone_list_hex,hex_side_length,height,width)








############################################################################

############################################################################





#DEFINE CONTROL BOARD CLASS
class ControlBoard:
    control_boards_list = []
    
    def __init__(self, playerObj, playerNo):
        self.control_boards_list.append(self)
        self.controlKeypointsCart = []
        self.control_detections = []
        self.col_hues = []
        self.col_sats = []
        self.col_vals = []

        
        self.playerNo = playerNo
        self.playerObj = playerObj

        #list opponent player nums
        self.opponent_player_nums = []
        self.temp_opponents = [1,2,3,4]
        for i in range(len(self.temp_opponents)):
            if self.temp_opponents[i] != self.playerNo:
                self.opponent_player_nums.append(self.temp_opponents[i])

        self.alliances_list=['OFF','OFF','OFF']
                
        
        self.techObj = Technology(self)
        self.techObj.refreshAvailableTech()

        self.owned_tech = []
        self.control_keypoints = []

        if self.playerNo == 1:
            self.startingxy = [0,0]
            self.direction = 1
            self.font_x_modifier = (240/10)*self.direction
        elif self.playerNo == 2:
            self.startingxy = [0,height/2]
            self.direction = 1
            self.font_x_modifier = (240/10)*self.direction
        elif self.playerNo == 3:
            self.startingxy = [width,0]
            self.direction = -1
            self.font_x_modifier = (280/2)*self.direction
        elif self.playerNo == 4:
            self.startingxy = [width,height/2]
            self.direction = -1
            self.font_x_modifier = (280/2)*self.direction

        self.ctrl_dots_list_xy = []
        for i in range(N_CTRL_DOTS):
            self.ctrl_dots_list_xy.append([self.startingxy[0]+(leftRightBuffer/15)*self.direction, self.startingxy[1]+ CTRL_DOT_DIST*(i+1)])


        self.labelx1 = self.ctrl_dots_list_xy[0][0] + self.font_x_modifier
        self.labely1 = max(self.ctrl_dots_list_xy[0][1] -45,0)
        self.labely2 = max(self.ctrl_dots_list_xy[3][1] ,0)
        self.labely3 = max(self.ctrl_dots_list_xy[4][1] ,0)
        self.labely4 = max(self.ctrl_dots_list_xy[5][1] ,0)

        

        self.tech1xy = [self.ctrl_dots_list_xy[0][0] + self.font_x_modifier,self.ctrl_dots_list_xy[0][1] -TECH_SIZE/2]
        self.tech2xy = [self.ctrl_dots_list_xy[1][0] + self.font_x_modifier,self.ctrl_dots_list_xy[1][1] -TECH_SIZE/2]
        self.tech3xy = [self.ctrl_dots_list_xy[2][0] + self.font_x_modifier,self.ctrl_dots_list_xy[2][1] -TECH_SIZE/2]
            
            
        print(self.ctrl_dots_list_xy)

                                     
    def drawCalibrationDots(self, screen, dotType, dotSize):
        for i in range(N_CTRL_DOTS):
            self.x = self.ctrl_dots_list_xy[i][0]
            self.y = self.ctrl_dots_list_xy[i][1]
            pygame.draw.ellipse(screen, (255,255,255), [self.x-(dotSize/2), self.y-(dotSize/2), dotSize, dotSize])

    def drawControlBoard(self):
        self.writeResoures()
        self.writeAlliances()

    def writeResoures(self):
        self.label1 = controlfont.render("Prd:"+str(self.playerObj.resource_P) + " Sci:"+str(self.playerObj.resource_S), 1, (255,100,20))
        screen.blit(self.label1, (self.labelx1, self.labely1))

    def writeAlliances(self):
        self.alliance_1_label = controlfont.render("Ally P"+str(self.opponent_player_nums[0])+ " "+str(self.alliances_list[0]), 1, (255,100,20))
        screen.blit(self.alliance_1_label, (self.labelx1, self.labely2 - 5))
        
        self.alliance_2_label = controlfont.render("Ally P"+str(self.opponent_player_nums[1])+ " "+str(self.alliances_list[1]), 1, (255,100,20))
        screen.blit(self.alliance_2_label, (self.labelx1, self.labely3 - 5))
        
        self.alliance_3_label = controlfont.render("Ally P"+str(self.opponent_player_nums[2])+ " "+str(self.alliances_list[2]), 1, (255,100,20))
        screen.blit(self.alliance_3_label, (self.labelx1, self.labely4 - 5))

    def randomTechOptions(self):
        self.random_tech_options = []
        self.random_tech_options = self.techObj.grabRandTech()

    def drawTech(self):
        if len(self.random_tech_options) >=1:
            screen.blit(self.random_tech_options[0][4], (self.tech1xy[0],self.tech1xy[1]))
        if len(self.random_tech_options) >=2:
            screen.blit(self.random_tech_options[1][4], (self.tech2xy[0],self.tech2xy[1]))
        if len(self.random_tech_options) >=3:
            screen.blit(self.random_tech_options[2][4], (self.tech3xy[0],self.tech3xy[1]))


    def applyCameraCalibration(self, kypts ):
        self.control_keypoints = kypts[:]

    def scanControlBoard(self, hsv_frames_list):
        self.control_detections = []
        
        for xy in self.control_keypoints:    
            if findShipId(hsv_frames_list,xy,SHIP_SEARCH_SIZE) == [1,0,0,0,0,0]:
                self.control_detections.append(1)
            else:
                self.control_detections.append(0)
        print("CONTROLDETECTIONS:", end = "")
        print(self.control_detections)

    def calibrateColours(self):
        camera.capture('colourCalibration.jpg')
        self.colrImg = cv2.imread('colourCalibration.jpg')
        print("colour calibraton image = ", self.colrImg)
        print("len colour calibraton image = ", len(self.colrImg))
        self.hsv_colrImg = cv2.cvtColor(self.colrImg, cv2.COLOR_BGR2HSV)
        print("hsv colour calibraton image = ", self.hsv_colrImg)
        print("len hsv colour calibraton image = ", len(self.hsv_colrImg))
        self.col_hues = []
        self.col_sats = []
        self.col_vals = []
        for xy in self.control_keypoints:
            self.ROI = self.hsv_colrImg[int(xy[0])][int(xy[1])]
            print("ROI ",self.ROI)
            print("xy range:"+ str(int(xy[0]-1)) + ' ' + str(int(xy[0]+1)))
            
            #print("newpix:")
            #print(pixx)
            self.col_hues.append(pixx[0])
            self.col_sats.append(pixx[1])
            self.col_vals.append(pixx[2])
            print("Reading colour calibration values")
            print("Hue " + str(pixx[0]))
            print("Sat " , pixx[1])
            print("Val " , pixx[2])
        """
            
            dftl = 27
saturtna = 30
vallua = 40
saturtnb = 255
vallub = 215
# DEFINE colour thresholds
hsvrng1a = np.array([0*179/360,saturtna,vallua])
hsvrng1ax = np.array([340*179/360,saturtna,vallua])
hsvrng2a = np.array([(60-dftl)*179/360,saturtna,vallua])
hsvrng3a = np.array([(120-dftl)*179/360,saturtna,vallua])
hsvrng4a = np.array([(180-dftl)*179/360,saturtna,vallua])
hsvrng5a = np.array([(240-dftl)*179/360,saturtna,vallua])
hsvrng6a = np.array([(290-dftl)*179/360,saturtna,vallua])
hsvrng1b = np.array([(dftl)*179/360,saturtnb,vallub])
hsvrng1bx = np.array([(359.9)*179/360,saturtnb,vallub])
hsvrng2b = np.array([(60+dftl)*179/360,saturtnb,vallub+20])
hsvrng3b = np.array([(120+dftl)*179/360,saturtnb,vallub])
hsvrng4b = np.array([(180+dftl)*179/360,saturtnb,vallub])
hsvrng5b = np.array([(240+dftl)*179/360,saturtnb,vallub])
hsvrng6b = np.array([(300+dftl)*179/360,saturtnb,vallub])
        """   

            

    def processControlBoardActions(self):
        self.alliances_list=['OFF','OFF','OFF']
        self.playerObj.alliances_playerNos = []
        self.playerObj.enemies_playerNos = []
        if len(self.control_detections)>0:
            #process alliances
            for i in range(3):
                if self.control_detections[i] == 1:
                    self.playerObj.alliances[i] = 1
                    self.alliances_list[i] = 'ON'
                    self.playerObj.alliances_playerNos.append(self.opponent_player_nums[i])
                else:
                    self.playerObj.enemies_playerNos.append(self.opponent_player_nums[i])
                    
            #process tech purchases
            for i in range(3):
                if self.control_detections[i+3] == 1:
                    self.techObj.buyTech(self.random_tech_options[i])



#DEFINE PLAYER CLASS
class Player:
    players_list = []
    
    def __init__(self, LocPlayer):
        self.players_list.append(self)

        self.LocPlayer = LocPlayer

        self.alliances = [0,0,0]
        self.alliances_playerNos = []
        self.enemies_playerNos = []

        self.xxyyzz = LocPlayer[:3]
        self.playerNo = LocPlayer[3]
        self.LocPlayerPos = LocPlayer[:]
        self.LocPlayerPos.append(0)
        
        self.resource_P = 1
        self.resource_S = 1
        self.resource_P_modifier = 1
        self.resource_S_modifier = 1

        self.plasma_defence = 0
        
        self.shipDamage = 1
        self.shipRepair = 1
        self.shipHealth = 60
        self.shipMaxHealth = 100
        self.shipSpeed = 1
        self.shipCost = 5
        self.shipScan = 0
        self.shipRange = 1
        self.planetHealth = 20
        self.planetMaxHealth = 100
        self.planetDamage = 1

        #self.planetTier = 0
        #self.shipTier = 0
        #self.randomTier = 0
        #self.resourceTier = 0

        self.controlBoard = ControlBoard(self, self.playerNo)
        self.controlBoard.playerObj = self
        
        self.Ships = []
        self.Planets = []
        
        #add ship at position zero
        #self.delme = self.addShip(self.LocPlayerPos,[self.shipDamage,self.shipRepair,self.shipHealth,self.shipSpeed])
        #add planet
        self.addPlanet(self.LocPlayer)

        
    def addShip(self,LocPlayerPos, shipId):
        self.DRHSS = [self.shipDamage,self.shipRepair,self.shipHealth,self.shipSpeed,self.shipScan]
        self.Ships.append(Ship(self,LocPlayerPos,self.DRHSS,shipId))
        return self.Ships[-1]
        
    def addPlanet(self, LocPlayer):
        self.Planets.append(Planet(self,LocPlayer))
        

    def collectResources(self):
        for planet in self.Planets:
            self.resource_P += planet.resource_P * self.resource_P_modifier
            self.resource_S += planet.resource_S * self.resource_S_modifier

    def deductShipCost(self):
        self.resource_P -= self.shipCost
       
       




#DEFINE PLANET CLASS
class Planet:
    planets_list = []
    
    def __init__(self, playerObject, LocPlayer):
        self.planets_list.append(self)

        self.owner = playerObject
        
        
        self.xxyyzz = LocPlayer[:3]
        self.xx = LocPlayer[0]
        self.yy = LocPlayer[1]
        self.zz = LocPlayer[2]
        self.playerNo = LocPlayer[3]

        
        self.resource_P = 1
        self.resource_S = 1

        
        if self.owner:
            self.maxHealth = self.owner.planetMaxHealth
            self.Health = self.owner.planetHealth
        else:
            self.maxHealth = 100
            self.Health = 20
            
        self.Damage = 1
        self.Repair = 1

        self.x, self.y = cubiToCart(self.xxyyzz)
        self.xy = [self.x, self.y]

        for x in hexesBigList:
            if x.xxyyzz == self.xxyyzz:
                x.addPlanet(self)
                self.hexObject = x
        
        #give planet the appropriate sprite. playerNo==0 is the default unoccupied planet
        self.planetSpriteLoc = pygame.transform.scale(pygame.image.load(os.path.join("Images", planet_image_list[self.playerNo])),(int(hex_side_length),int(hex_side_length)))
        #for kk in range(0,NPLAYERS+1):
        #    if self.playerNo == kk:
        #        self.planetSpriteLoc = pygame.transform.scale(pygame.image.load(os.path.join("Images", planet_image_list[kk])),(int(hex_side_length),int(hex_side_length)))

    def drawPlanet(self, screen):
        if self.Health <0:
            self.Health = 0
        screen.blit(self.planetSpriteLoc, (self.x - int(hex_side_length)/2, self.y - int(hex_side_length)/2))
        pygame.draw.circle(screen, (int(250*(1-min(self.Health/self.maxHealth,1))),int(250*min(self.Health/self.maxHealth,1)),0), [int(self.x), int(self.y)], 30, 1)
        self.label1 = shipfont.render(str(self.Damage), 1, (255,255,255))
        screen.blit(self.label1, (self.x-3, self.y-17))

    
    def updatePlanetTech(self):
        self.maxHealth = self.owner.planetMaxHealth
        self.Damage = self.owner.planetDamage
        

    def transferControl(self, newPlayerNum):
        #remove self from list of old owner's planets
        if self.owner:
            self.owner.Planets.remove(self)
        self.playerNo = newPlayerNum
        #add new owner and add self ot list of new owners planets
        for x in Player.players_list:
            if x.playerNo == self.playerNo:
                self.owner = x
                x.Planets.append(self)
        #give planet the appropriate sprite
        self.planetSpriteLoc = pygame.transform.scale(pygame.image.load(os.path.join("Images", planet_image_list[self.playerNo])),(int(hex_side_length),int(hex_side_length)))
    




#DEFINE TECHNOLOGY CLASS
class Technology:
    tech_list = []
    
    def __init__(self, controlBoardObj):
        self.tech_list.append(self)

        self.controlBoardObj = controlBoardObj
        self.playerObj = controlBoardObj.playerObj
        
        self.owned_tech = []
        self.available_tech = []
        #print("AVAILAVBLE TECH:", end="")
        #print(self.available_tech)
        

        self.planet_itci  = [['pl',"P_01_01.jpg",1,3],['pl',"P_01_02.jpg",2,5],['pl',"P_01_03.jpg",3,7],['pl',"P_02_01.jpg",1,3],['pl',"P_02_02.jpg",2,5],['pl',"P_02_03.jpg",3,7]]
        self.ship_itci    = [['sh',"S_01_01.jpg",1,3],['sh',"S_01_02.jpg",2,5],['sh',"S_01_03.jpg",3,7],['sh',"S_02_01.jpg",1,3],['sh',"S_02_02.jpg",2,5],['sh',"S_02_03.jpg",3,7],['sh',"S_03_01.jpg",1,3],['sh',"S_04_01.jpg",1,3],['sh',"S_04_02.jpg",2,5],['sh',"S_04_03.jpg",3,7],['sh',"S_05_03.jpg",3,7],['sh',"S_06_02.jpg",2,3]]
        self.random_itci  = [['ra',"X_07_01.jpg",1,3],['ra',"X_07_02.jpg",2,5],['ra',"X_07_03.jpg",3,7]]
        self.resource_itci= [['re',"R_08_01.jpg",1,3],['re',"R_08_02.jpg",2,5],['re',"R_08_03.jpg",3,7],['re',"R_09_01.jpg",1,3],['re',"R_09_02.jpg",2,5],['re',"R_09_03.jpg",3,7]]


        
        for i in range(len(self.planet_itci)):
            self.planet_itci[i].append(self.imageify(self.planet_itci[i][1]))
            self.planet_itci[i].append(i)
        for i in range(len(self.ship_itci)):
            self.ship_itci[i].append(self.imageify(self.ship_itci[i][1]))
            self.ship_itci[i].append(i)
        for i in range(len(self.random_itci)):
            self.random_itci[i].append(self.imageify(self.random_itci[i][1]))
            self.random_itci[i].append(i)
        for i in range(len(self.resource_itci)):
            self.resource_itci[i].append(self.imageify(self.resource_itci[i][1]))
            self.resource_itci[i].append(i)
            

        self.planet_tier_unlocked, self.ship_tier_unlocked, self.random_tier_unlocked, self.resource_tier_unlocked = 1,1,1,1

        self.full_tech_list = self.planet_itci + self.ship_itci + self.random_itci + self.resource_itci
                                        

    def imageify(self, tech):
        return pygame.transform.scale(pygame.image.load(os.path.join("Images/Tech", tech)),(TECH_SIZE,TECH_SIZE)) 

    def refreshAvailableTech(self):
        self.available_tech = []

        #add techs which are unlocked and not yet owned
        print("TECH:")
        for tech in self.full_tech_list:
            print(tech)
            if tech[0] == 'pl' and tech[2] <= self.planet_tier_unlocked and tech not in self.owned_tech:
                self.available_tech.append(tech)
            elif tech[0] == 'sh' and tech[2] <= self.ship_tier_unlocked and tech not in self.owned_tech:
                self.available_tech.append(tech)
            elif tech[0] == 'ra' and tech[2] <= self.random_tier_unlocked and tech not in self.owned_tech:
                self.available_tech.append(tech)
            elif tech[0] == 're' and tech[2] <= self.resource_tier_unlocked and tech not in self.owned_tech:
                self.available_tech.append(tech)
                
    def grabRandTech(self):
        self.random_tech = []
        self.refreshAvailableTech()
        
        print("AVAILTECH:")
        print(self.available_tech)
        
        if len(self.available_tech) >= 3:
            self.random_tech = random.sample(self.available_tech,3)
        elif len(self.available_tech) == 2:
            self.random_tech = random.sample(self.available_tech,2)
        elif len(self.available_tech) == 1:
            self.random_tech = random.sample(self.available_tech,1)

        print("RANDOMTECH:")
        print(self.random_tech)
        return self.random_tech



    def buyTech(self,tech=None):
        if tech != None:
            self.playerObj.resource_S -= tech[3]
            self.owned_tech.append(tech)
            
            if tech[0] == 'pl':
                #unlock tech tier
                if tech[2] >= self.planet_tier_unlocked:
                    self.planet_tier_unlocked +=1
                #process tech abilities
                if tech[5] == 1:
                    self.playerObj.planetDamage +=1
                elif tech[5] == 2:
                    self.playerObj.planetDamage +=1
                elif tech[5] == 3:
                    self.playerObj.planetDamage +=2
                elif tech[5] == 4:
                    self.playerObj.planetMaxHealth +=50
                elif tech[5] == 5:
                    self.playerObj.planetMaxHealth +=50
                elif tech[5] == 6:
                    self.playerObj.planetMaxHealth +=75
                    
            elif tech[0] == 'sh':
                #unlock tech tier
                if tech[2] >= self.ship_tier_unlocked:
                    self.ship_tier_unlocked +=1
                #process tech abilities
                if tech[5] == 1:
                    self.playerObj.shipDamage += 1
                elif tech[5] == 2:
                    self.playerObj.shipDamage += 1
                elif tech[5] == 3:
                    self.playerObj.shipDamage += 2
                elif tech[5] == 4:
                    self.playerObj.shipMaxHealth += 50
                elif tech[5] == 5:
                    self.playerObj.shipMaxHealth += 50
                elif tech[5] == 6:
                    self.playerObj.shipMaxHealth += 75
                elif tech[5] == 7:
                    self.playerObj.shipScan += 1
                elif tech[5] == 8:
                    self.playerObj.shipRepair += 1
                elif tech[5] == 9:
                    self.playerObj.shipRepair += 1
                elif tech[5] == 10:
                    self.playerObj.shipRepair += 1
                elif tech[5] == 11:
                    self.playerObj.shipRange += 1
                elif tech[5] == 12:
                    self.playerObj.shipSpeed += 1
                    
            elif tech[0] == 'ra':
                #unlock tech tier
                if tech[2] >= self.random_tier_unlocked:
                    self.random_tier_unlocked +=1
                #process tech abilities
                if tech[5] == 1:
                    self.playerObj.plasma_defence += 1
                elif tech[5] == 2:
                    self.playerObj.plasma_defence += 1
                elif tech[5] == 3:
                    self.playerObj.plasma_defence += 2
                    
            elif tech[0] == 're':
                #unlock tech tier
                if tech[2] >= self.resource_tier_unlocked:
                    self.resource_tier_unlocked +=1
                #process tech abilities
                if tech[5] == 1:
                    self.playerObj.resource_S_modifier += 1
                elif tech[5] == 2:
                    self.playerObj.resource_S_modifier += 1
                elif tech[5] == 3:
                    self.playerObj.resource_S_modifier += 1
                elif tech[5] == 4:
                    self.playerObj.resource_P_modifier += 1
                elif tech[5] == 5:
                    self.playerObj.resource_P_modifier += 1
                elif tech[5] == 6:
                    self.playerObj.resource_P_modifier += 1
        
    



#DEFINE SHIP CLASS
class Ship:
    ships_list = []
    
    def __init__(self, playerObj, LocPlayerPos, DRHSS, shipId):
        self.ships_list.append(self)

        self.playerObj = playerObj
        
        self.xxyyzz = LocPlayerPos[:3]
        self.xx = LocPlayerPos[0]
        self.yy = LocPlayerPos[1]
        self.zz = LocPlayerPos[2]
        self.playerNo = LocPlayerPos[3]
        self.shipPos = LocPlayerPos[4]

        self.DRHSS = DRHSS

        self.Damage = DRHSS[0]
        self.Repair = DRHSS[1]
        self.Health = DRHSS[2]
        self.Speed = DRHSS[3]
        self.Scan = DRHSS[4]
        self.Range = playerObj.shipRange

        self.maxHealth = self.playerObj.shipMaxHealth

        self.shipId = shipId

        self.Destroyed = 0

        self.ship_targets = []
        self.planet_targets = []

        
        self.x, self.y = cubiToCart(self.xxyyzz)
        self.xy = [self.x, self.y]

        for x in hexesBigList:
            if x.xxyyzz == self.xxyyzz:
                x.addShip(self)
                self.HexObject = x
        
        for x in playersBigList:
            if x.playerNo == self.playerNo:
                self.playerObj = x
        
        #give ship the appropriate sprite. playerNo==0 is the default unoccupied planet
        self.shipSpriteLoc = pygame.transform.scale(pygame.image.load(os.path.join("Images", ship_image_list[self.playerNo])),(ship_size[0],ship_size[1]))
        #for kk in range(0,NPLAYERS+1):
        #    if self.playerNo == kk:
        #        self.shipSpriteLoc = pygame.transform.scale(pygame.image.load(os.path.join("Images", ship_image_list[kk])),(ship_size[0],ship_size[1]))
                #self.planetSpriteLoc = pygame.image.load(os.path.join("Images", planet_image_list[kk]))

    def drawShip(self, screen):
        screen.blit(self.shipSpriteLoc, (self.HexObject.shipDrawVerts[self.shipPos][0] - ship_size[0]/2, self.HexObject.shipDrawVerts[self.shipPos][1] - ship_size[1]/2))
        #screen.blit(self.shipSpriteLoc, (self.HexObject.shipDrawVerts[1][0] - ship_size[0]/2, self.HexObject.shipDrawVerts[1][1] - ship_size[1]/2))
        #screen.blit(self.shipSpriteLoc, (self.HexObject.shipDrawVerts[2][0] - ship_size[0]/2, self.HexObject.shipDrawVerts[2][1] - ship_size[1]/2))
        #label1 = myfont.render('D:' + str(self.Damage), 1, (0,255,255))
        #label2 = myfont.render('S:' + str(self.Speed), 1, (255,255,200))
        self.label1 = shipfont.render(str(self.Damage), 1, (255,255,255))
        self.label2 = shipfont.render(str(self.Speed), 1, (255,255,255))
        screen.blit(self.label1, (self.HexObject.shipDrawVerts[self.shipPos][0]-3, self.HexObject.shipDrawVerts[self.shipPos][1]-10))
        screen.blit(self.label2, (self.HexObject.shipDrawVerts[self.shipPos][0]-3, self.HexObject.shipDrawVerts[self.shipPos][1]))
        self.scanSurroundings()

    def drawHealthbar(self, screen):
        if self.Health<0:
            self.Health = 0
        pygame.draw.circle(screen, (int(250*(1-min(self.Health/self.maxHealth,1))),int(250*min(self.Health/self.maxHealth,1)),0), [int(self.HexObject.shipDrawVerts[self.shipPos][0]), int(self.HexObject.shipDrawVerts[self.shipPos][1])], 11, 1)

    def destroyShip(self):
        if self.Destroyed == 0:
            self.ships_list.remove(self)
            self.playerObj.Ships.remove(self)
            if self in self.HexObject.ship_objects:
                self.HexObject.ship_objects.remove(self)
            if self in self.ships_list:
                self.ships_list.remove(self)
                
            #self.HexObject.shipIds.remove(self.shipId)
            for i in range(len(self.HexObject.shipIds)):
                if self.HexObject.shipIds[i]==self.shipId:
                    self.HexObject.shipIds.pop(i)
                    break
            for i in range(len(self.HexObject.players_present)):
                if self.HexObject.players_present[i]==self.playerNo:
                    self.HexObject.players_present.pop(i)
                    break
            self.Destroyed = 1
            self.Damage = 0
            self.shipId = [0,0,0,0,0,0]
        else:
            self.Destroyed = 1
            
        """
        for item in self.HexObject.players_present:
            if item == self.playerNo:
                self.HexObject.players_present.remove(item)
        """

    def scanSurroundings(self):
        if self.playerNo > 0:
            if self.Scan == 1:
                self.nbrs = findNeighbours(self.xxyyzz)
                self.nbrs.append(self.xxyyzz)
                for x in hexesBigList:
                    if x.xxyyzz in self.nbrs:
                        x.visible = 2
            else:
                self.HexObject.visible = 2

    def updateLocation(self):
        
        self.xxyyzz = self.HexObject.xxyyzz
        self.xx = self.HexObject.xx
        self.yy = self.HexObject.yy
        self.zz = self.HexObject.zz

        self.x = self.HexObject.x
        self.y = self.HexObject.y
        self.xy = [self.x, self.y]

    def updateHexObjectShipslist(self):
        
        self.HexObject.players_present.append(self.playerNo)
        self.HexObject.ship_objects.append(self)
        self.HexObject.shipIds.append(self.shipId)
        


#DEFINE HEX CLASS
class HexClass:
    hexes_list = []
    def __init__(self, xxyyzz):
        self.hexes_list.append(self)
        
        self.xxyyzz = xxyyzz
        self.xx = xxyyzz[0]
        self.yy = xxyyzz[1]
        self.zz = xxyyzz[2]

        self.x, self.y = cubiToCart(self.xxyyzz)

        self.planetExists = 0
        self.Planet = False
        self.shipExists = [0,0,0]
        self.ship_objects = []
        self.visible = 0
        self.prevShipIds = []
        self.shipIds = []
        

        self.players_present = []

        self.hexVerts = []
        for degsyy in range(0,301,60):
            self.hexVerts.append([self.x + hex_side_length * math.cos(math.radians(degsyy)), self.y + hex_side_length * math.sin(math.radians(degsyy))])

        self.shipDrawVerts = []
        for degsyy in range(0,301,120):
            self.shipDrawVerts.append([self.x + hex_side_length*3/5 * math.cos(math.radians(degsyy)), self.y + hex_side_length*3/5 * math.sin(math.radians(degsyy))])
            print(self.shipDrawVerts[-1])

        self.shipFindVerts = []
        for degsyy in range(60,301,120):
            self.shipFindVerts.append([self.x + hex_side_length*3/5 * math.cos(math.radians(degsyy)), self.y + hex_side_length*3/5 * math.sin(math.radians(degsyy))])

        self.camx = [0,0]
        self.triKeypointLocs = []
        #self.triKeypointLocs = [[0,0],[0,0],[0,0]]
        
    def drawmelikeoneofyourfrenchgirls(self, screen, i):
        pygame.draw.polygon(screen, (66,i*.9,i*.3), self.hexVerts, self.visible)
        
    def drawCalibrationDots(self, dotType, dotSize):
        if dotType == 0:
            pygame.draw.ellipse(screen, (255,255,255), [self.x-(dotSize/2), self.y-(dotSize/2), dotSize, dotSize])
        if dotType in range(1,4):
            x = dotType - 1
            pygame.draw.ellipse(screen, (255,255,255), [self.shipFindVerts[x][0]-(dotSize/2), self.shipFindVerts[x][1]-(dotSize/2), dotSize, dotSize])
    
    def applyCameraCalibration(self, centerKeypoint, triKeypointLocs1, triKeypointLocs2, triKeypointLocs3):
        self.camxy = centerKeypoint[:]
        self.triKeypointLocs = []
        self.triKeypointLocs.append(triKeypointLocs1)
        self.triKeypointLocs.append(triKeypointLocs2)
        self.triKeypointLocs.append(triKeypointLocs3)

    def drawDots(self, screen, dotSize, i):
        if self.visible > -1:
        #if self.visible:
            #center dot
            pygame.draw.ellipse(screen, (96,i*.9,i*.4), [self.x-(dotSize/2), self.y-(dotSize/2), dotSize, dotSize])
            #triscan dots
            for x in range(0,3):
                pygame.draw.ellipse(screen, (i,i,i), [self.shipFindVerts[x][0]-(dotSize/2), self.shipFindVerts[x][1]-(dotSize/2), dotSize, dotSize])
                #pygame.draw.ellipse(screen, (0,i,0), [self.shipFindVerts[x][0]-(dotSize/2), self.shipFindVerts[x][1]-(dotSize/2), dotSize, dotSize])

    def addPlanet(self,planetObj):
        self.Planet = planetObj
        self.planetExists = 1

    def addShip(self, ship):
        self.ship_objects.append(ship)
        #self.shipExists[position] = 1

    def scanForShips(self, hsv_frames_list):
        self.prevShipIds = self.shipIds[:]
        self.players_present = []
        self.shipIds = []
        self.ship_objects = []
        self.temp_ship_objects = []
        self.locindex = 0
        for xy in self.triKeypointLocs:
            self.locindex +=1
            self.shipId = findShipId(hsv_frames_list,xy,SHIP_SEARCH_SIZE)

            #if there even is a ship there
            if self.shipId != [0,0,0,0,0,0]:
                #self.shipIds.append(self.shipId)
        
                self.shipFound = 0
                #find matching ship
                if Ship.ships_list:
                    for ship in Ship.ships_list:
                        if self.shipId == ship.shipId:
                            #self.ship_objects.append(ship)
                            ship.shipPos = self.locindex - 1
                            ship.HexObject = self
                            self.shipFound = 1
                            ship.updateLocation()
                #if matching ship not found, create ship in the relevant location
                if self.shipFound == 0:
                    for player in Player.players_list:
                        if self.xxyyzz == player.xxyyzz:
                            player.LocPlayerPos[4] = self.locindex - 1 #update the player temp indicator for verticy location, which is passed to ships
                            self.temp_ship_objects.append(player.addShip(player.LocPlayerPos, self.shipId))
                            self.temp_ship_objects[-1].HexObject = self #tell ship what hex it is in
                            player.deductShipCost()





#DEFINE PLASMA STORM CLASS
class PlasmaStorm:
    plasma_storm_list = []
    
    def __init__(self, HexObject, turnCounter):
        self.plasma_storm_list.append(self)

        self.HexObject = HexObject
        self.xxyyzz = HexObject.xxyyzz
        self.xx = HexObject.xxyyzz[0]
        self.yy = HexObject.xxyyzz[1]
        self.zz = HexObject.xxyyzz[2]

        self.exists = 1

        self.x, self.y = cubiToCart(self.xxyyzz)
        self.turnCounter = turnCounter

        self.damage = randint(1,self.turnCounter)
        self.duration = randint(2,8)
        if self.duration >5:
            self.img = "X_07_03.jpg"
        elif self.duration>3:
            self.img = "X_07_02.jpg"
        else:
            self.img = "X_07_01.jpg"
        self.plasmaImage = pygame.transform.scale(pygame.image.load(os.path.join("Images/Tech", self.img)),(PLASMA_STORM_SIZE,PLASMA_STORM_SIZE)) 


    def damageShips(self, ship_objects_list):
        for ship in ship_objects_list:
            if ship.xxyyzz == self.xxyyzz:
                ship.Health -= ship.Health - int(self.damage / (ship.playerObj.plasma_defence +1))

    def drawPlasmaStorm(self):
        screen.blit(self.plasmaImage, (self.x - PLASMA_STORM_SIZE/2, self.y - PLASMA_STORM_SIZE/2))

    def processDuration(self):
        self.duration -=1
        if self.duration >5:
            self.img = "X_07_03.jpg"
        elif self.duration>3:
            self.img = "X_07_02.jpg"
        else:
            self.img = "X_07_01.jpg"
        self.plasmaImage = pygame.transform.scale(pygame.image.load(os.path.join("Images/Tech", self.img)),(PLASMA_STORM_SIZE,PLASMA_STORM_SIZE)) 
        if self.duration == 0:
            for i in range(len(PlasmaStorm.plasma_storm_list)):
                if PlasmaStorm.plasma_storm_list[i] == self:
                    self.exists = PlasmaStorm.plasma_storm_list.pop(i)
                    break
            self.damage = 0
            self.exists = 0




"""
    def updateHexShipsPresent():
        self.players_present = []
        self.shipIds = []
        self.ship_objects = []
        if Ship.ships_list:
            for ship in Ship.ships_list:
                if ship.xxyyzz == self.xxyyzz:
                    
                    self.shipIds.append(ship.shipId)
                    self.ship_objects.append(ship)
                
            if self.ship_objects:
                #compile a list of ship owners (players_present)
                for x in range(0,len(self.ship_objects)):
                    self.players_present.append(self.ship_objects[x].playerNo)
"""                            



#######################################################################
    #######################################################################

# SORT ZONE_LIST_HEX..... by left -> right (already done) then by up -> down
zone_list_hex2 = list(zone_list_hex)
zone_list_hex_sortedtmp = []
zone_list_hex_sorted = []
for i in range(1,BOARD_COLUMNS+1):
    for k in range(1, board_columns_rows[i-1] +1):
        zone_list_hex_sortedtmp.append(zone_list_hex2.pop(0))
        #print('k3:', i)
    zone_list_hex_sortedtmp.sort(key=lambda x: x[1], reverse=True)
    for k in range(1, board_columns_rows[i-1] + 1):
        zone_list_hex_sorted.append(zone_list_hex_sortedtmp.pop(0))
        #print('k4:', i)

#print('zone_list_hex_sorted:', zone_list_hex_sorted)




#CALIBRATE BLOBS WITH CAMERA, BLOB 0 = CENTER DOT; BLOB 1-3 = TRIDOT
def blobCalibrator(blobNum, dotSize):
    
    keypoints_cart_tmp = []
    
    blobSuccess = 0

    while blobSuccess == 0:

        try:
            screen.fill(black)
            pygame.display.flip()
            time.sleep(4) # allow time to adjust game surface

            #calibrate camera HIFRIEND REPLACE THE IMAGE CAPTURES!
            camera.capture('backgroundImage.jpg')
            for hexx in hexesBigList:
                hexx.drawCalibrationDots(blobNum,dotSize)
            pygame.display.flip()
            camera.capture('foregroundImage.jpg')
            backgroundSubtraction()
            keypoints_cart_tmp, keypoints = blobDetection()

            if len(keypoints_cart_tmp) == NTOTAL_HEXES:
                blobSuccess = 1
                print("[SUCCESS] : Blob Detection. That's sexy!")
            else:
                blobSuccess = 0
                print("[FAIL]: INCORRECT NUMBER OF BLOBS DETECTED!")
                print("Found: ", len(keypoints_cart_tmp))
                print("Expected: ", NTOTAL_HEXES)

        except:
            print("[FAIL]: BLOB DETECTION RUNTIME ERROR!!!")
            print("Trying again in 3...", end = "")
            time.sleep(1)
            print(" 2...", end = "")
            time.sleep(1)
            print(" 1")
            time.sleep(1)
            #print("Detected %s blobs, when there should have been
            blobSuccess = 0
            
   

    #sort keypoints by left -> right then by up -> down
    #print('keypoints_cart:', keypoints_cart)
    keypoints_cart_tmp.sort(key=lambda x: x[0], reverse=False)
    #print('keypoints_cart sorted:', keypoints_cart)

    keypoints_cart2 = list(keypoints_cart_tmp)
    keypoints_cart_sortedtmp = []
    keypoints_cart_sorted = []
    for i in range(1,BOARD_COLUMNS+1):
        for k in range(1, board_columns_rows[i-1] +1):
            keypoints_cart_sortedtmp.append(keypoints_cart2.pop(0))
            #print('k1:', k)
        keypoints_cart_sortedtmp.sort(key=lambda x: x[1], reverse=False)
        for k in range(1, board_columns_rows[i-1] + 1):
            keypoints_cart_sorted.append(keypoints_cart_sortedtmp.pop(0))
            #print('k2:', k)

    return keypoints_cart_sorted

    
    
#CREATE ALL HEX OBJECTS
hexesBigList = []
for i in range(0,NTOTAL_HEXES):
    hexesBigList.append(HexClass(zone_list_hex_sorted[i][0:3]))



keypoints_cart = []
keypoints_cart_tri = []

#CALIBRATE ALL HEX OBJECTS
def calibrateAllHexObjects():
    keypoints_cart = blobCalibrator(0,12)
    keypoints_cart_tri.append(blobCalibrator(1,12))
    keypoints_cart_tri.append(blobCalibrator(2,12))
    keypoints_cart_tri.append(blobCalibrator(3,12))
    return keypoints_cart, keypoints_cart_tri
keypoints_cart, keypoints_cart_tri = calibrateAllHexObjects()


#CALIBRATE ALL HEXES WITH CAMPOINTS
for i in range(0,NTOTAL_HEXES):
    hexesBigList[i].applyCameraCalibration(keypoints_cart[i], keypoints_cart_tri[0][i], keypoints_cart_tri[1][i], keypoints_cart_tri[2][i])

print("hexes calibrated")
print(hexesBigList[0].triKeypointLocs[0])
print(hexesBigList[0].triKeypointLocs[1])
print(hexesBigList[0].triKeypointLocs[2])




#CREATE ALL PLAYER OBJECTS (init call to create rel planets and ships)
playersBigList = []
for x in LocPlayer:
    playersBigList.append(Player(x))
print("playersCreated")





#
#
#             CALIBRATE ALL CONTROL BOARD BLOBS HERE
#
#


#CALIBRATE CONTROL BLOBS WITH CAMERA, BLOB 0 = CENTER DOT; BLOB 1-3 = TRIDOT
def controlBlobCalibrator(playerObj, dotSize):
    
    keypoints_cart_tmp = []
    
    blobSuccess = 0

    
    while blobSuccess == 0:

        try:
            screen.fill(black)
            pygame.display.flip()
            #time.sleep(4) # allow time to adjust game surface

            #calibrate camera HIFRIEND REPLACE THE IMAGE CAPTURES!
            camera.capture('backgroundImage.jpg')
            
            playerObj.controlBoard.drawCalibrationDots(screen,1,dotSize)
            pygame.display.flip()
            camera.capture('foregroundImage.jpg')
            backgroundSubtractionControl()
            keypoints_cart_tmp, keypoints = blobDetectionControl()

            if len(keypoints_cart_tmp) == 6:
                blobSuccess = 1
                print("[SUCCESS] : Control Blob Detection. That's sexy!")
            else:
                blobSuccess = 0
                print("[FAIL]: INCORRECT NUMBER OF Control BLOBS DETECTED!")
                print("Found: ", len(keypoints_cart_tmp))
                print("Expected: ", NTOTAL_HEXES)

        except:
            print("[FAIL]: Control BLOB DETECTION RUNTIME ERROR!!!")
            print("Trying again in 3...", end = "")
            time.sleep(1)
            print(" 2...", end = "")
            time.sleep(1)
            print(" 1")
            time.sleep(1)
            #print("Detected %s blobs, when there should have been
            blobSuccess = 0
            
   

    #sort keypoints by up -> down
    #print('keypoints_cart:', keypoints_cart)
    print('controlboard keypoints sorted:', keypoints_cart_tmp)
    keypoints_cart_tmp.sort(key=lambda x: x[1], reverse=False)
    print('controlboard keypoints sorted:', keypoints_cart_tmp)

    return keypoints_cart_tmp

    
    
for x in Player.players_list:
    #x.controlBoard.controlKeypointsCart = controlBlobCalibrator(x, 12)
    x.controlBoard.applyCameraCalibration(controlBlobCalibrator(x, 12))
print("control dots calibrated")













#CREATE ALL UNOWNED PLANET OBJECTS
outer_planets_list = []
for xxx in extraPlanets:
    #xxxa = xxx[:].append(0)
    outer_planets_list.append(Planet(None, xxx))
print("extraplanetsCreated")





#play game initiation sound
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("Sounds", "space.mp3"))
pygame.mixer.music.play()


#make planet tiles visible
for x in Planet.planets_list:
    if x.playerNo >0:
        x.hexObject.visible = 2


    #########################################################################
########################################################################
playerTurnInd = randint(1,NPLAYERS)
playerTurnLabel = controlfont.render("PLAYER " +str(playerTurnInd) +" TURN", 1, (255,255,255))
ControlBoard.control_boards_list[playerTurnInd-1].randomTechOptions()


plasma_storm_list = []
keyCountdown = 1
colorDirxn=1
i=1
turnCounter = 1
while 1:

    #CHECK FOR SCREEN CLOSURE
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    #HANDLE KEY PRESSES
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]: sys.exit()
    if pressed_keys[pygame.K_SPACE]:
        print(pressed_keys[pygame.K_SPACE])
        for x in hexesBigList:
            if x.visible == 0:
                x.visible = 2
            elif x.visible == 2:
                x.visible = 0
        time.sleep(.2)
    if pressed_keys[pygame.K_c]:
        print(pressed_keys[pygame.K_c])
        #display 6 dots
        print("displaying colour calibration dots")
        screen.blit(bgb, (0,0))
        pygame.display.flip()
        ControlBoard.control_boards_list[0].drawCalibrationDots(screen,1,22)
        pygame.display.flip()
        time.sleep(5)
        #scan 6 dots
        print("scanning 6 control colour dots")
        ControlBoard.control_boards_list[0].calibrateColours()
        #update colours
        print("updating colours with calibration")
        setColourThresholds()
        time.sleep(.2)
    if pressed_keys[pygame.K_RETURN]:
        print(pressed_keys[pygame.K_RETURN])
        turnCounter += 1

        print("Checking for Winner")
        winner = checkWinCondition(turnCounter)
        if winner!=None:
            screen.blit(bgb, (0,0))
            playerTurnLabel = controlfont.render(winner, 1, (255,255,255))
            screen.blit(playerTurnLabel, (width/2-50, 20))
            pygame.display.flip()
            time.sleep(10)
            
        
        print("Processing Ship Movement")
        processShipMoves()

        
        for x in Planet.planets_list:
            x.drawPlanet(screen)

        for x in Ship.ships_list:
            x.drawHealthbar(screen)
            x.drawShip(screen)

        for x in hexesBigList:
            x.drawmelikeoneofyourfrenchgirls(screen, i)
            x.drawDots(screen,6,i)

        
        pygame.display.flip()
        time.sleep(1)

        
        print("CollectingResources")
        for x in Player.players_list:
            x.collectResources()

        
        print("Buying Tech")
        for x in ControlBoard.control_boards_list:
            if x.playerNo == playerTurnInd:
                x.scanControlBoard(hsv_frames_list)
                x.processControlBoardActions()

        print("Processing Plasma Storm Damage & Duration")
        if PlasmaStorm.plasma_storm_list:
            for x in PlasmaStorm.plasma_storm_list:
                x.damageShips(Ship.ships_list)
                x.processDuration()
        deleteDestroyedShips()
            
        print("Processing Combat")
        processShipCombat()
        processPlanetCombat()
        processLongRangeShipVsPlanetCombat()

        
        for x in Planet.planets_list:
            x.drawPlanet(screen)

        for x in Ship.ships_list:
            x.drawHealthbar(screen)
            x.drawShip(screen)

        for x in hexesBigList:
            x.drawmelikeoneofyourfrenchgirls(screen, i)
            x.drawDots(screen,6,i)

        
        pygame.display.flip()
        time.sleep(1)

        print("Processing planet captures")
        processPlanetCaptures()

        
        for x in Planet.planets_list:
            x.drawPlanet(screen)

        for x in Ship.ships_list:
            x.drawHealthbar(screen)
            x.drawShip(screen)

        for x in hexesBigList:
            x.drawmelikeoneofyourfrenchgirls(screen, i)
            x.drawDots(screen,6,i)

        
        pygame.display.flip()
        time.sleep(1)
        
        print("Ships & planets self repairing")
        shipSelfRepair()
        planetSelfRepair()

        
        for x in Planet.planets_list:
            x.drawPlanet(screen)

        for x in Ship.ships_list:
            x.drawHealthbar(screen)
            x.drawShip(screen)

        for x in hexesBigList:
            x.drawmelikeoneofyourfrenchgirls(screen, i)
            x.drawDots(screen,6,i)
        
        
        pygame.display.flip()
        time.sleep(1)



        print("Updating player turn indicator")
        playerTurnInd +=1
        if playerTurnInd>NPLAYERS:
            playerTurnInd = 1

        playerTurnLabel = controlfont.render("PLAYER " +str(playerTurnInd) +" TURN", 1, (255,255,255))
        ControlBoard.control_boards_list[playerTurnInd-1].randomTechOptions()


        print("Generating New Plasma Storms")
        for x in hexesBigList:
            if randint(2,1500) < turnCounter:
                print("StormCreated!!")
                plasma_storm_list.append(PlasmaStorm(x,turnCounter))        
        
        time.sleep(0.5)
        
    #MAKE HEXGRID PHASE IN AND OUT
    i+=7*colorDirxn
    if i>255:
        i=255
        colorDirxn=-1
    if i<1:
        i=0
        colorDirxn=1
        
    #make background black
    #screen.fill(black)
    #paint backgroud image
    screen.blit(bgb, (0,0))

   





        
    for x in Planet.planets_list:
        x.drawPlanet(screen)
        if x.owner != None:
            x.updatePlanetTech()

    for x in hexesBigList:
        if x.Planet:
            if x.Planet.owner != None:
                if x.Planet.owner.playerNo >0:
                    x.visible = 2
        else: x.visible = 0

    for x in Ship.ships_list:
        x.drawHealthbar(screen)
        x.drawShip(screen)

    for x in hexesBigList:
        x.drawmelikeoneofyourfrenchgirls(screen, i)
        x.drawDots(screen,6,i)

    for x in Player.players_list:
        x.controlBoard.drawCalibrationDots(screen,1,22)
        x.controlBoard.drawControlBoard()

    if PlasmaStorm.plasma_storm_list:
        for x in PlasmaStorm.plasma_storm_list:
            x.drawPlasmaStorm()

    ControlBoard.control_boards_list[playerTurnInd-1].drawTech()
    screen.blit(playerTurnLabel, (width/2-50, 20))
    

    pygame.display.flip()

    #for x in hexesBigList:
#    x.visible = 0
