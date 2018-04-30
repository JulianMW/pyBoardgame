from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import sys, pygame
from modules2 import *
import csv
import math
from PIL import Image



#generate a list of hex center locations in the hex coordinate sytem
def generateCubicHex(BOARD_SIZE):
    zone_list_hex=[]
    for x in range(-BOARD_SIZE,BOARD_SIZE+1):
        for y in range(-BOARD_SIZE,BOARD_SIZE+1):
            for z in range(-BOARD_SIZE,BOARD_SIZE+1):
                
                if x+y+z==0:
                    zone_list_hex.append([x,y,z])
                    #print(x,y,z)
    return zone_list_hex
    


#define cartesian location of hex centers in pixels
def generateCartHex(zone_list_hex,hex_side_length,height,width):
    zone_pixels_cart=[]
    for liste in zone_list_hex:
        xx = liste[0] * (3/2) * hex_side_length + width/2
        yy =  math.sqrt(3) * hex_side_length * (liste[0]/2 + liste[1]) + height/2
        zone_pixels_cart.append([xx,yy])
    return zone_pixels_cart



#given x,y .. return all verticies of relevant hexagon
#starts at right and goes clockwise
def generateHexVerts(x,y,hex_side_length):
    
    degsyy = 0
    x1= x + hex_side_length * math.cos(math.radians(degsyy))
    y1= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 60
    x2= x + hex_side_length * math.cos(math.radians(degsyy))
    y2= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 120
    x3= x + hex_side_length * math.cos(math.radians(degsyy))
    y3= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 180
    x4= x + hex_side_length * math.cos(math.radians(degsyy))
    y4= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 240
    x5= x + hex_side_length * math.cos(math.radians(degsyy))
    y5= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 300
    x6= x + hex_side_length * math.cos(math.radians(degsyy))
    y6= y + hex_side_length * math.sin(math.radians(degsyy))
    
    return [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5],[x6,y6]]



#define cartesian location of hex centers in pixels
def drawGrid(screen,zone_pixels_cart,i,hex_side_length):
    for polyg in zone_pixels_cart:
        pygame.draw.polygon(screen,(22,i*.9/2,i*.3/2), generateHexVerts(polyg[0],polyg[1],hex_side_length),0)


#define cartesian location of hex centers in pixels
def drawDots(screen,zone_pixels_cart,dotSize):
    for polyg in zone_pixels_cart:
        pygame.draw.ellipse(screen, (255,255,255), [polyg[0]-(dotSize/2), polyg[1]-(dotSize/2), dotSize, dotSize])

def backgroundSubtraction():
    image1 = Image.open('foregroundImage.jpg')
    image2 = Image.open('backgroundImage.jpg')

    image1.load()
    image2.load()
    image3 = image1._new(image1.im.chop_subtract(image2.im, 1.0, 0))

    image3.save('subtractedImage.jpg')



def backgroundSubtractionControl():
    """
    image1 = Image.open('foregroundImage.jpg')
    image2 = Image.open('backgroundImage.jpg')

    image1.load()
    image2.load()
    image3 = image1._new(image1.im.chop_subtract(image2.im, 1.0, 0))

    image3.save('subtractedImage.jpg')
    """
    pass



def blobDetection():
    im = cv2.imread("subtractedImage.jpg", cv2.IMREAD_GRAYSCALE)
    
    # Setup SimpleBlobDetector parameters.
 
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 256
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 20

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5
     
    # Filter by Inertia
    params.filterByInertia =True
    params.minInertiaRatio = 0.5

    # Change colout
    params.filterByColor = True
    params.maxThreshold = 256

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)



    # Detect blobs.
    keypoints = detector.detect(255-im)
    keypoints_cart = []
    print("numKeypoints= ", len(keypoints))

    for keypt in range(0,len(keypoints)):
        x = keypoints[keypt].pt[0]
        y = keypoints[keypt].pt[1]
        print("x=", x)
        print("y=", y)
        print(" ")
        keypoints_cart.append([x,y])
        
        
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Show keypoints
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)
    cv2.imwrite('detectedBlobs.png',im_with_keypoints)
    return keypoints_cart, keypoints



def blobDetectionControl():
    im = cv2.imread("subtractedImageControl.jpg", cv2.IMREAD_GRAYSCALE)
    
    # Setup SimpleBlobDetector parameters.
 
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 256
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 20

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5
     
    # Filter by Inertia
    params.filterByInertia =True
    params.minInertiaRatio = 0.5

    # Change colout
    params.filterByColor = True
    params.maxThreshold = 256

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)



    # Detect blobs.
    keypoints = detector.detect(255-im)
    keypoints_cart = []
    print("numKeypoints= ", len(keypoints))

    for keypt in range(0,len(keypoints)):
        x = keypoints[keypt].pt[0]
        y = keypoints[keypt].pt[1]
        print("x=", x)
        print("y=", y)
        print(" ")
        keypoints_cart.append([x,y])
        
        
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Show keypoints
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)
    cv2.imwrite('detectedBlobsControl.png',im_with_keypoints)
    return keypoints_cart, keypoints





#HSL Detection - given an image array in hsv it will output the identity of any ship theredetected
# for opencv For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. 
hue=0
hue = hue/360 *179

"""
#hues = [x for x in range(0,361,60)]
hues_list = [0,60,120,180,240,300]
def findShipId(hsvImageArray,hueRange):
    out_array = [0,0,0,0,0,0]
    numPixels = len(hsvImageArray) 
    pixel_sum = [0,0,0,0,0,0] #keeps track of the count of each hue-matching pixel
    for pixx in hsvImageArray:
        for hueCnt in range(0,6):
            #if ( ((pixx[0] + 60) > (hues_list[hueCnt] +60 - hueRange)) and ((pixx[0] + 60) < (hues_list_looped[hueCnt] +60 + hueRange))  ):
            elif ( ((pixx[0]%330) > (hues_list[hueCnt] +60 - hueRange)) and ((pixx[0] + 60) < (hues_list_looped[hueCnt] +60 + hueRange))  ):
                if ( (pixx[1] > 150) and (pixx[2] > 150) ):
                    pixel_sum[hueCnt] +=1
    for i in range(0,5):
        if pixel_sum[i] > numPixels/24:
            out_array[i] = 1
    print("Detected shipId", out_array)
    return out_array


#GENTERATE SHIP IDENTIFIERS
import itertools
from itertools import combinations


#Hifriend generate sh ip identifiers - 6 hues w/ 4colour die
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



#CREATE SHIP COLOUR COMBINATIONS
lst1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
lst = []
for x in lst1:
    lst.append(x*60)
combs = []
#aaaa = [list(x) for x in combinations(lst, 4)]
#for x in range(len(aaaa)): combs.append(aaaa[x])
aaaa = [list(x) for x in combinations(lst, 3)]
for x in range(len(aaaa)): combs.append(aaaa[x])
aaaa = [list(x) for x in combinations(lst, 2)]
for x in range(len(aaaa)): combs.append(aaaa[x])

print(len(combs), end=" ships created")


"""
