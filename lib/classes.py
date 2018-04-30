import math
import pygame
from statistics import mean
import numpy as np
import time
from itertools import chain
import os
import cv2
import logging



class Zones:
    instances_list = []
    def __init__(self, n_colours = 5, width = 1200, height = 900, control_width = 180, board_size = 3):
        self.instances_list.append(self)
        self.n_colours = n_colours
        self.dimensions = [0, 0, width, height] # x_0,y_0,x_f,y_f
        self.height = height
        self.width = width
        self.control_width = control_width
        self.board_size = board_size
        self.mask_loc_names = []
        self.dot_size = 6
        self.num_columns = board_size * 2 + 1
        self.control_board_dimensions_list = [[0, 0, self.control_width, self.height/2],
                                 [0, self.height/2, self.control_width, self.height],
                                 [self.width - self.control_width, 0, self.width, self.height/2],
                                 [self.width - self.control_width, self.height/2, self.width, self.height]]
        
        
        # Where to draw/detect colour calibration squares
        self.colr_cal_xy = []
        for i in range(self.n_colours):
            self.colr_cal_xy.append([self.width / (self.n_colours + 2) * (i + 1), self.height / 2])
            
        self.camera_dot_locations = []
        for i in range(len(self.colr_cal_xy)):
            self.camera_dot_locations.append([0,0])
            
        self.colour_thresholds = []
        for i in range(len(self.colr_cal_xy)):
            self.colour_thresholds.append([0,0,0])
    
    
    def draw_colour_calibration_squares(self, screen):
        self.recsz = 50
        for xy in self.colr_cal_xy:
            pygame.draw.rect(screen, (255,255,255), (int(xy[0]-self.recsz/2),int(xy[1]-self.recsz/2),self.recsz,self.recsz))
    
    def draw_colour_calibration_dots(self, screen, dotSize):
        for xy in self.colr_cal_xy:
            pygame.draw.circle(screen, (255,255,255), (int(xy[0]),int(xy[1])), int(dotSize), 0)
    
    def average_hsv_calibration(self, screen, flip, camera, cv2, size, iso_val, brightness, IMAGE_CAPTURE_DELAY):
        screen.fill((0, 0, 0))
        self.draw_colour_calibration_squares(screen)
        flip()
        inpu = input('ready?')
        camera.ISO=iso_val
        #screen.fill((255, 255, 255))
        screen.fill((brightness,brightness,brightness))
        flip()
        time.sleep(IMAGE_CAPTURE_DELAY)
        camera.capture_image('ColourMasterImage.jpg')
        #time.sleep(0.1)
        camera.ISO = 0
        self.tempimg =  cv2.imread('ColourMasterImage.jpg')
        self.coloursImage = cv2.blur(self.tempimg, (2,2))
        
        # extract ROI, convert to HSV, extract hsv pixel values, then average those pixel values into average_hsv_list
        self.average_hsv_list = []
        for i, xy in enumerate(self.camera_dot_locations):
            self.roi = self.coloursImage[int(xy[1]-size):int(xy[1]+size), int(xy[0]-size):int(xy[0]+size)]
            #roi = img[r1:r2, c1:c2]
            self.hsv_roi = cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)

            #use numpy to average over rows and columns of pixels
            self.avgcolrow = np.average(self.hsv_roi, axis=0)
            self.avgavgcolrow = np.average(self.avgcolrow, axis=0)
            self.average_hsv_list.append( [round(x) for x in np.ndarray.tolist(self.avgavgcolrow )] )

        print("Average HSV values for 6 colours detected are:")
        print(self.average_hsv_list)
        self.calibrate_colour_thresholds()
            
        
    
    def calibrate_colour_thresholds(self, h_range = 12, s_range = 80, v_range = 80):
        self.colour_thresholds = []
        # H: 0 to 179 S: 0 to 255 V: 0 to 255
        for c, x in enumerate(self.average_hsv_list):
            self.min_sat = 80
            self.min_val = 60
            self.max_sat = 255
            self.max_val = 255
            self.lower_thresh = np.array([max(x[0] - h_range,0), self.min_sat, self.min_val], dtype = "uint16")
            self.upper_thresh = np.array([min(x[0] + h_range,179), self.max_sat, self.max_val], dtype = "uint16")
            
            #self.lower_thresh = np.array([max(x[0] - h_range,0), max(x[1] - s_range,0), max(x[2] - v_range,0)], dtype = "uint16")
            #self.upper_thresh = np.array([min(x[0] + h_range,179), min(x[1] + s_range,255), min(x[2] + v_range,255)], dtype = "uint16")
            self.colour_thresholds.append([self.lower_thresh,self.upper_thresh])
                                          
            


class ControlBoards:
    instances_list = []
    #def __init__(self, dimensions, playerObj):
    def __init__(self, dimensions):
        self.instances_list.append(self)
        self.player_object = None
        self.dimensions = dimensions # x_0,y_0,x_f,y_f
        self.num_control_dots = 6
        
        self.height = dimensions[3] - dimensions[1]
        self.width = dimensions[2] - dimensions[0]
        
        #set control title location
        self.title_location = [self.dimensions[0] + 1, self.dimensions[1] + 1]
        
        self.font_type = pygame.font.SysFont("monospace", 16)
        
        #set control dot size & locations
        self.dot_size = int(self.height/16)
        self.control_dot_locations = []
        for i in range(1,7):
            self.control_dot_locations.append([self.dimensions[0] + self.width * 0.1, self.dimensions[1] + (i/7) * self.height])
        
        #set tech draw size & locations
        self.tech_draw_size = int(self.height/7)
        self.tech_draw_locations = []
        for i in range(1,7):
            self.tech_draw_locations.append([self.dimensions[0] + self.width * 0.3, self.dimensions[1] + (i/7) * self.height])

        #self.inter_dot_distance_y = self.tech_draw_locations[2,1] - self.tech_draw_locations[1,1] 
        
        #initialize camera dot locations to 0,0
        self.camera_dot_locations = []
        for i in range(1,7):
            self.camera_dot_locations.append([0,0])
        
        
    def describe_self(self):
        print("Hello I am a ControlBoard instance")
        print("My dimensions are: ", end='')
        print(self.dimensions)
        
    def draw_control_dots(self, screen, i, dotSize):
        for x in range(0,6):
            #i = i * 1.2 +5
            #i = min(255, i)
            pygame.draw.circle(screen, (255,255,i), tuple(map(round,self.control_dot_locations[x])), dotSize, 0)
        
    def calibrate_control_dots(self, coords):
        self.camera_dot_locations = coords
        
    def print_title(self, screen, playerNum, sci, prod, font_colour):
        self.text = self.font_type.render("Player " + str(playerNum) + "  Prd:"+str(prod) + "  Sci:"+str(sci), 1, font_colour)
        screen.blit(self.text, tuple(self.title_location))
        
    def print_allies(self, screen):
        for j , xy in enumerate(self.tech_draw_locations):
            if j>2:
                if j-2 < self.player_object.player_num:
                    if self.player_object.alliances_list and int(j-2) in self.player_object.alliances_list:
                        self.text = self.font_type.render("Ally P"+str(j-2)+" ON", 1, (255,255,255))
                        screen.blit(self.text, (int(xy[0] +self.player_object.tech_object.width/2 + 1), int(xy[1] - self.player_object.tech_object.width/2)) )
                    else:
                        self.text = self.font_type.render("Ally P"+str(j-2)+" OFF", 1, (255,255,255))
                        screen.blit(self.text, (int(xy[0] +self.player_object.tech_object.width/2 + 1), int(xy[1] - self.player_object.tech_object.width/2)) )
                else:
                    if self.player_object.alliances_list and int(j-1) in self.player_object.alliances_list:
                        self.text = self.font_type.render("Ally P"+str(j-1)+" ON", 1, (255,255,255))
                        screen.blit(self.text, (int(xy[0] +self.player_object.tech_object.width/2 + 1), int(xy[1] - self.player_object.tech_object.width/2)) )
                    else:
                        self.text = self.font_type.render("Ally P"+str(j-1)+" OFF", 1, (255,255,255))
                        screen.blit(self.text, (int(xy[0] +self.player_object.tech_object.width/2 + 1), int(xy[1] - self.player_object.tech_object.width/2)) )
    
    def read_control_dots(self, loaded_mask_list, logging, scansize = 10):
        #scans dots and returns an array of length self.num_control_dots containing a 1 if dot was detected and a 0 otherwise
        self.out_array = [0 for i in range(self.num_control_dots)]
        self.pixel_sum = [0 for i in range(self.num_control_dots)] #keeps track of the count of each hue-matching pixel
        for dotnum , xy in enumerate(self.camera_dot_locations):
            #print("xy ",xy)
            self.ROI = loaded_mask_list[0][int(xy[1]-scansize):int(xy[1]+scansize), int(xy[0]-scansize):int(xy[0]+scansize)]
            self.ROI_height, self.ROI_width = self.ROI.shape[:2]
            self.numPixels = self.ROI_height * self.ROI_width
            self.pixel_sum[dotnum] = cv2.countNonZero(self.ROI)
            if self.pixel_sum[dotnum] > self.numPixels/8:
                self.out_array[dotnum] = 1
            #print("detected " + str(self.pixel_sum[dotnum]) + " / " + str(self.numPixels) + " pixels for control dot " + str(dotnum))
            logging.debug("detected " + str(self.pixel_sum[dotnum]) + " / " + str(self.numPixels) + " pixels for control dot " + str(dotnum))
        return self.out_array
    



# Create Hex Tiles
# DEFINE HEX CLASS
class HexTiles:
    instances_list = []
    buffer_size = 1
    neighbour_transforms = [[0,0,0],[1,-1,0],[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1]]
    
    @classmethod
    def initialize_class_params(cls, GameBoard):
        
        cls.buffer_size = cls.buffer_size * (GameBoard.board_size)

        # edge_radius = HEX_EDGE_DIST
        cls.edge_radius = min(GameBoard.width - GameBoard.control_width*2, GameBoard.height - cls.buffer_size) / ( (GameBoard.board_size*2+1)*2 )

        # side_length = HEX_SIDE_LENGTH
        cls.side_length = cls.edge_radius / (math.cos(math.radians(30)))

        # create rows_in_col_num, a list of #rows in each column
        cls.rows_in_col_num = []
        for i in range(1, GameBoard.board_size + 2):
            cls.rows_in_col_num.append(i + GameBoard.board_size)
        for i in range(1, GameBoard.board_size + 1):
            cls.rows_in_col_num.append(GameBoard.num_columns - i)

        cls.edge_diameter = 2 * cls.edge_radius
        cls.vertice_radius = cls.side_length / 2
        cls.vertice_diameter = cls.side_length
    
    
    def __init__(self, xxyyzz, conversions, GameBoard):
        self.instances_list.append(self)
        
        self.xxyyzz = xxyyzz
        self.xy = list(conversions.cubic_to_cart(self.xxyyzz, HexTiles, GameBoard))
        
        #what column does this hex tile fall in. Range = [1,GameBoard.num_columns]
        self.column = self.xxyyzz[0] + GameBoard.board_size  + 1
        if self.xxyyzz[0] <=0:
            self.row = - self.xxyyzz[2] + GameBoard.board_size + 1
        else:
            self.row = self.xxyyzz[1] + GameBoard.board_size + 1
        
        self.visible = 0
        
        self.vertices = []
        for degsyy in range(0,301,60):
            self.vertices.append([self.xy[0] + HexTiles.side_length * math.cos(math.radians(degsyy)), self.xy[1] + HexTiles.side_length * math.sin(math.radians(degsyy))])
        
        self.shipDrawVerts = []
        #for degsyy in range(0 + self.phase_shift, 301 + self.phase_shift, 120):
        for degsyy in range(240, -1, -120):
            self.shipDrawVerts.append([self.xy[0] + HexTiles.side_length*3/5 * math.cos(math.radians(degsyy)), self.xy[1] + HexTiles.side_length*3/5 * math.sin(math.radians(degsyy))])
            
        self.shipFindVerts = []
        #for degsyy in range(60 + self.phase_shift, 301 + self.phase_shift, 120):
        for degsyy in range(300, -1, -120):
            self.shipFindVerts.append([self.xy[0] + HexTiles.side_length*3/5 * math.cos(math.radians(degsyy)), self.xy[1] + HexTiles.side_length*3/5 * math.sin(math.radians(degsyy))])
            
        self.shipFindVerts_cam = []
        #for degsyy in range(60 + self.phase_shift, 301 + self.phase_shift, 120):
        for degsyy in range(300, -1, -120):
            self.shipFindVerts_cam.append([0,0])
        
        #self.camx = [0,0]
        #self.triKeypointLocs = []
        
    def initialize_neighbour_objects(self, GameBoard, HexTiles):
        self.neighbours_object_list = []
        self.neighbours_xxyyzz_list = []
        for x in HexTiles.neighbour_transforms:
            self.a = [self.xxyyzz[i] + x[i] for i in range(len(self.xxyyzz))]
            if max(self.a) <= GameBoard.board_size:
                self.neighbours_xxyyzz_list.append(self.a)
        for neighbour_xxyyzz in self.neighbours_xxyyzz_list:
            for hex in HexTiles.instances_list:
                if hex.xxyyzz == neighbour_xxyyzz:
                    self.neighbours_object_list.append(hex)
        
    def print_description(self):
        print("I'm at cubic coordinates:" , end='')
        print(self.xxyyzz)
        print("Cartesian coordinates: ", end='')
        print(self.xy)
        print("Row " + str(self.row) + ", Col " + str(self.col))
        print("With camera shipdetect vertice coordinates:")
        print(self.shipFindVerts_cam)
        
        pygame.draw.polygon(screen, (66,i*.9,i*.3), self.vertices, self.visible)
        
    def drawmelikeoneofyourfrenchgirls(self, screen, i):
        pygame.draw.polygon(screen, (66,i*.9,i*.3), self.vertices, self.visible)
        
    def drawDots(self, screen, i, dotSize):
        #if self.visible:
        #center dot
        if self.visible == 0:
            pygame.draw.circle(screen, (26,i*.3,i*.2), tuple(map(round,self.xy)), dotSize, 0)
        #triscan dots
        for x in range(0,3):
            pygame.draw.circle(screen, (26,i,i), tuple(map(round,self.shipFindVerts[x])), dotSize, 0)
    """
    def draw_detection_dots(self, screen, i, dotSize):
        if self.visible > 0:
            for x in range(0,3):
                pygame.draw.circle(screen, (255,255,255), tuple(map(round,self.shipFindVerts[x])), dotSize, 0)
    """
    def drawIndividualShipFindVerts(self, screen, i, dotSize, x):
        pygame.draw.circle(screen, (i, i, i), tuple(map(round,self.shipFindVerts[x])), dotSize, 0)
        
    def detect_ships(self, GameBoard, loaded_mask_list, logging, scansize = 8):
        self.ship_ids_list = []
        self.ship_vertice_list = []
        self.ship_draw_xy = []
        self.self_hex_list = []
        for vertnum , xy in enumerate(self.shipFindVerts_cam):
            #print("XY in shipFindVerts = " , xy)
            self.out_array = [0 for i in range(GameBoard.n_colours)]
            self.pixel_sum = [0 for i in range(GameBoard.n_colours)] #keeps track of the count of each hue-matching pixel
            for i in range(len(self.out_array)):
                self.ROI = loaded_mask_list[i][int(xy[1]-scansize):int(xy[1]+scansize), int(xy[0]-scansize):int(xy[0]+scansize)]
                self.numPixels = self.ROI.size
                self.pixel_sum[i] = cv2.countNonZero(self.ROI)
                if self.pixel_sum[i] > self.numPixels/16:
                    self.out_array[i] = 1
                    
            # check if there's a ship of >4 colours detected... if so then return the ship with the 4 most prevalent colours
            if sum(self.out_array)>4:
                logging.warning("IMPOSSIBLE NUMBER OF COLOURS DETECTED IN SHIP")
                logging.debug("Attempting to correct impossible ship")
                self.pixel_sum_copy = [x for x in self.pixel_sum]
                self.pixel_sum_copy.sort(reverse=True)
                for x in range(len(self.out_array)):
                    if self.pixel_sum[x] >= self.pixel_sum_copy[3]:
                        self.out_array[x] = 1
                    else:
                        self.out_array[x] = 0
            if sum(self.out_array)>4:
                print("UNABLE TO RESOLVE IMPOSSIBLE SHIP DETECTION")
                logging.warning("UNABLE TO RESOLVE IMPOSSIBLE SHIP DETECTION")
                logging.debug("UNABLE TO RESOLVE IMPOSSIBLE SHIP DETECTION")
                
            # if there's at least one colour detected, output as a ship
            if any(v != 0 for v in self.out_array):
                self.ship_ids_list.append(self.out_array)
                self.ship_vertice_list.append(vertnum)
                self.self_hex_list.append(self)
                print('Detected the following ships: %s', self.ship_ids_list)
                print('  and column: %s', self.column)
                print('  in row: %s', self.row)
                print('  and vertice' + str(vertnum))
                logging.debug('Detected the following ships: %s', self.ship_ids_list)
                logging.debug('  and column: %s', self.column)
                logging.debug('  in row: %s', self.row)
                logging.debug('  and vertice %s' , str(vertnum))
        return self.ship_ids_list , self.ship_vertice_list,  self.self_hex_list
    
