import numpy as np
import cv2
from PIL import Image
import time
import sys


def blob_detection():
    #load image as greyscale
    im = cv2.imread("subtracted_image.jpg", cv2.IMREAD_GRAYSCALE)
    
    #apply binary thresholding (whites==>fullwhite, darks==>fulldark)
    _,im1 = cv2.threshold(im,40,255,cv2.THRESH_BINARY)

    #apply dilation to image
    kernel = np.ones((3,3),np.uint8)
    im = cv2.dilate(im1, kernel, iterations = 1)
    
    # Setup SimpleBlobDetector parameters
    
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 256
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 40

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.4
     
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




def cam_coords_sorted(num_blobs_expected, 
                      foreground_image_nm='foregroundImage.jpg', 
                      background_image_nm='backgroundImage.jpg', 
                      sort_direction = 'vertical', 
                      num_fail_retries = 3):
    
    detected_blobs = 0

    keypoints_cart = []

    # Perform background subtraction on two images
    foreground_image = Image.open(foreground_image_nm)
    background_image = Image.open(background_image_nm)

    foreground_image.load()
    background_image.load()
    subtracted_image = foreground_image._new(foreground_image.im.chop_subtract(background_image.im, 1.0, 0))

    subtracted_image.save('subtracted_image.jpg')

    # Invoke blob detection
    keypoints_cart, keypoints = blob_detection()
    print(keypoints_cart)

    detected_blobs = len(keypoints_cart)

    if detected_blobs != num_blobs_expected:
        success_ind = False
        print("FAILED TO DETECT CORREC NUMBER OF BLOBS... retrying")
    else:
        success_ind = True
        print("Successfully detected " +str(num_blobs_expected) + " blobs!")
            
    
    # Return camera coordinates list in form [[x1,y1],[x2,y2],...] sorted either vertically or horizontally
    if sort_direction == 'vertical':
        keypoints_cart.sort(key=lambda x: x[1])
        return keypoints_cart, success_ind
        #return keypoints_cart.sort(key=lambda x: x[1])
    else:
        keypoints_cart.sort(key=lambda x: x[0])
        return keypoints_cart, success_ind
        


def calibrate_gameboard_dots(x, screen, displayflip, capture_image, test_ind = 0):
    
    # x == GameBoard
        
    # How many times to retry if incorrect # blobs detected
    for retries in range(4):

        if test_ind == 0:
            #display black
            screen.fill((0, 0, 0))
            displayflip()

            #capture background image
            capture_image('backgroundImage.jpg')

            #draw dots
            x.draw_colour_calibration_dots(screen, 6)
            displayflip()

            #capture foreground image
            capture_image('foregroundImage.jpg')

        # call horizontal blob detector
        # cam_coords_sorted(num_blobs_expected, foreground_image_nm='foregroundImage.jpg', background_image_nm='backgroundImage.jpg', sort_direction = 'vertical', num_fail_retries = 2)
        keypoints_cart, success_ind = cam_coords_sorted(x.n_colours, sort_direction = 'horizontal')

        if success_ind:
            break
    if not success_ind:
        print("maximum number of failed dot-detections reached.... exiting")
        sys.exit()

    #update control board's camera coordinates
    #x.calibrate_colour_dots(keypoints_cart)
    x.camera_dot_locations = keypoints_cart
        
        
def calibrate_control_dots(ControlBoards, screen, displayflip, capture_image, test_ind = 0):
    
    for x in ControlBoards.instances_list:
        
        # How many times to retry if incorrect # blobs detected
        for retries in range(4):
        
            if test_ind == 0:
                #display black
                screen.fill((0, 0, 0))
                displayflip()

                #capture background image
                capture_image('backgroundImage.jpg')

                #draw dots
                x.draw_control_dots(screen, 255, 6)
                displayflip()

                #capture foreground image
                capture_image('foregroundImage.jpg')

            # call vertical blob detector
            # cam_coords_sorted(num_blobs_expected, foreground_image_nm='foregroundImage.jpg', background_image_nm='backgroundImage.jpg', sort_direction = 'vertical', num_fail_retries = 2)
            keypoints_cart, success_ind = cam_coords_sorted(6)
            
            if success_ind:
                break
        if not success_ind:
            print("maximum number of failed dot-detections reached.... exiting")
            sys.exit()
        
        #update control board's camera coordinates
        x.calibrate_control_dots(keypoints_cart)
        

        

# Loop over 3 ship verts, and then over columns, assigning cam coordinates to relevant hex
# This will call the blob detector (num_columns * 3) times
def calibrate_hex_dots_slow(GameBoard, HexTiles, screen, displayflip, capture_image):
    
    # Loop over columns
    for col in range(GameBoard.num_columns):
        rel_hexes_list = []

        # extract list of relevant hexes, sorted by their row
        for hex in HexTiles.instances_list:
            if hex.column == col + 1:
                rel_hexes_list.append(hex)
        rel_hexes_list.sort(key=lambda x: x.row)

        # Loop over the 3 ship find verts
        for i in range(3):
            
            for retries in range(2):
                #draw and get row-sorted cam coords of all ship verts i in column col
                screen.fill((0, 0, 0))
                displayflip()
                capture_image('backgroundImage.jpg')
                for hex in rel_hexes_list:
                    hex.drawIndividualShipFindVerts(screen, 255, 8, i)
                displayflip()
                capture_image('foregroundImage.jpg')
                keypoints_cart, success_ind = cam_coords_sorted(HexTiles.rows_in_col_num[col])
                if success_ind:
                    break
            if not success_ind:
                print("maximum number of failed dot-detections reached.... exiting")
                sys.exit()
            
            # set relevant hex shipFindVerts_cam to coordinates of that hex
            for j in range(len(keypoints_cart)):
                rel_hexes_list[j].shipFindVerts_cam[i] = keypoints_cart.pop(0)

                

# Loop over the columns assigning cam coordinates to relevant hex
# This will call the blob detector (num_columns) times
# this relies on a finer top-down coordinate detection distance
def calibrate_hex_dots_fast(GameBoard, HexTiles, screen, displayflip, capture_image):
    
    # Loop over columns
    for col in range(GameBoard.num_columns):
        rel_hexes_list = []

        # extract list of relevant hexes, sorted by their row
        for hex in HexTiles.instances_list:
            if hex.column == col + 1:
                rel_hexes_list.append(hex)
        rel_hexes_list.sort(key=lambda x: x.row)

            
        #how many times to retry if incorrect # blobs detected
        for retries in range(4):
            
            #draw and get row-sorted cam coords of all ship verts i in column col
            screen.fill((0, 0, 0))
            displayflip()
            capture_image('backgroundImage.jpg')

            # draw all ship find verts in the relevant column
            for hex in rel_hexes_list:
                for i in range(3):
                    hex.drawIndividualShipFindVerts(screen, 255, 8, i)
            displayflip()
            capture_image('foregroundImage.jpg')
            keypoints_cart, success_ind = cam_coords_sorted(HexTiles.rows_in_col_num[col] * 3)
            
            if success_ind:
                break
        if not success_ind:
            print("maximum number of failed dot-detections reached.... exiting")
            sys.exit()

        # set relevant hex shipFindVerts_cam to coordinates of that hex
        for hex in rel_hexes_list:
            for i in range(3):
                hex.shipFindVerts_cam[i] = keypoints_cart.pop(0)

        
"""
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


#takes in a r
def setColourThresholds(dftl = 20,saturtna = 60,vallua = 60,saturtnb = 255,vallub = 155,sat_dftl = 20,val_dftl = 20):

    if ControlBoard.control_boards_list[0].col_hues[0] < dftl:
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),
                             int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360, 
                             int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([( 360 - dftl + ControlBoard.control_boards_list[0].col_hues[0])*180/360  , 
                              int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  360  )*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    elif ControlBoard.control_boards_list[0].col_hues[0] > (360 - dftl):
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360, 
                             int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0] - dftl)*180/360  , 
                              int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  dftl - (360 -  ControlBoard.control_boards_list[0].col_hues[0])  )*180/360, 
                              int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    else:
        hsvrng1a = np.array([(ControlBoard.control_boards_list[0].col_hues[0]
                              -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] -
                                                 sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0]
                               -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] -
                                                  sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0] +
                              dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] +
                                                sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1bx = np.array([(ControlBoard.control_boards_list[0].col_hues[0] +
                               dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] +
                                                 sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        
                            
        

    #hsvrng1a =  np.array([  0,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    #hsvrng1ax = np.array([340*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    
    hsvrng2a = np.array([(ControlBoard.control_boards_list[0].col_hues[1]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    hsvrng3a = np.array([(ControlBoard.control_boards_list[0].col_hues[2]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[2]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[2]/2)])
    hsvrng4a = np.array([(ControlBoard.control_boards_list[0].col_hues[3]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[3]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[3]/2)])
    hsvrng5a = np.array([(ControlBoard.control_boards_list[0].col_hues[4]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[4]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[4]/2)])
    hsvrng6a = np.array([(ControlBoard.control_boards_list[0].col_hues[5]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[5]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[5]/2)])

    #hsvrng1b =  np.array([(dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    #hsvrng1bx = np.array([(359.9)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    
    hsvrng2b = np.array([(ControlBoard.control_boards_list[0].col_hues[1]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[1]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    hsvrng3b = np.array([(ControlBoard.control_boards_list[0].col_hues[2]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[2]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[2]+20)])
    hsvrng4b = np.array([(ControlBoard.control_boards_list[0].col_hues[3]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[3]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[3]+20)])
    hsvrng5b = np.array([(ControlBoard.control_boards_list[0].col_hues[4]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[4]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[4]+20)])
    hsvrng6b = np.array([(ControlBoard.control_boards_list[0].col_hues[5]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[5]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[5]+20)])
"""



"""
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
    
"""





#Below are the old methods for calibrating hex dots IN THE MAIN.PY FILE.
#They have since been moved into calibrate namespace
"""

# Loop over 3 ship verts, and then over columns, assigning cam coordinates to relevant hex
# This will call the blob detector (num_columns * 3) times
def calibrate_hex_dots_slow():
    
    # Loop over columns
    for col in range(GameBoard.num_columns):
        rel_hexes_list = []

        # extract list of relevant hexes, sorted by their row
        for hex in HexTiles.instances_list:
            if hex.column == col + 1:
                rel_hexes_list.append(hex)
        rel_hexes_list.sort(key=lambda x: x.row)

        # Loop over the 3 ship find verts
        for i in range(3):
            
            for retries in range(2):
                #draw and get row-sorted cam coords of all ship verts i in column col
                screen.fill((0, 0, 0))
                pygame.display.flip()
                cam.capture_image('backgroundImage.jpg')
                for hex in rel_hexes_list:
                    hex.drawIndividualShipFindVerts(screen, 255, 8, i)
                pygame.display.flip()
                cam.capture_image('foregroundImage.jpg')
                keypoints_cart, success_ind = calibrate.cam_coords_sorted(HexTiles.rows_in_col_num[col])
                if success_ind:
                    break
            
            # set relevant hex shipFindVerts_cam to coordinates of that hex
            for j in range(len(keypoints_cart)):
                rel_hexes_list[j].shipFindVerts_cam[i] = keypoints_cart.pop(0)

#calibrate_hex_dots_slow()

# Loop over the columns assigning cam coordinates to relevant hex
# This will call the blob detector (num_columns) times
# this relies on a finer top-down coordinate detection distance
def calibrate_hex_dots_fast():
    
    # Loop over columns
    for col in range(GameBoard.num_columns):
        rel_hexes_list = []

        # extract list of relevant hexes, sorted by their row
        for hex in HexTiles.instances_list:
            if hex.column == col + 1:
                rel_hexes_list.append(hex)
        rel_hexes_list.sort(key=lambda x: x.row)

            
        #how many times to retry if incorrect # blobs detected
        for retries in range(2):
            
            #draw and get row-sorted cam coords of all ship verts i in column col
            screen.fill((0, 0, 0))
            pygame.display.flip()
            cam.capture_image('backgroundImage.jpg')

            # draw all ship find verts in the relevant column
            for hex in rel_hexes_list:
                for i in range(3):
                    hex.drawIndividualShipFindVerts(screen, 255, 8, i)
            pygame.display.flip()
            cam.capture_image('foregroundImage.jpg')
            keypoints_cart, success_ind = calibrate.cam_coords_sorted(HexTiles.rows_in_col_num[col] * 3)
            
            if success_ind:
                    break

        # set relevant hex shipFindVerts_cam to coordinates of that hex
        for hex in rel_hexes_list:
            for i in range(3):
                hex.shipFindVerts_cam[i] = keypoints_cart.pop(0)

#calibrate_hex_dots_fast()
"""

    
"""
#FUNCTION DEFINITIONS
def cubiToCart(xxyyzz):
    x = xxyyzz[0]  * (3/2) * HexTiles.side_length + GameBoard.width/2
    y = math.sqrt(3) * HexTiles.side_length * (xxyyzz[0]/2 + xxyyzz[1]) + GameBoard.height/2
    return x, y
"""

 
"""
def calibrate_control_dots(test_ind = 0):
    for x in ControlBoards.instances_list:
        
        #how many times to retry if incorrect # blobs detected
        for retries in range(2):
        
            if test_ind == 0:
                #display black
                screen.fill((0, 0, 0))
                pygame.display.flip()

                #capture background image
                cam.capture_image('backgroundImage.jpg')

                #draw dots
                x.draw_control_dots(screen, 255, 6)
                pygame.display.flip()

                #capture foreground image
                cam.capture_image('foregroundImage.jpg')

            #call vertical blob detector
            # cam_coords_sorted(num_blobs_expected, foreground_image_nm='foregroundImage.jpg', background_image_nm='backgroundImage.jpg', sort_direction = 'vertical', num_fail_retries = 2)
            keypoints_cart, success_ind = calibrate.cam_coords_sorted(6)
            
            if success_ind:
                break
        
        #update control board's camera coordinates
        x.calibrate_control_dots(keypoints_cart)
        #print(keypoints_cart)
        #print(list(keypoints_cart))
"""


