# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import numpy as np


# Initialize Camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(1) # allow the camera to warmup
#camera.ISO=100


camera.resolution = (1280, 720)
camera.framerate = 20
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

camera.iso = 400
camera.shutter_speed = 100000
#camera.analog_gain = 1
#camera.digital_gain = 1
#camera.exposure_mode = 'off'
#cam.exposure_compensation = 0
#camera.awb_mode = 'off'
#camera.awb_gains = (0,0)
#cam.awb_gains = g

# initialize the camera and grab a reference to the raw camera capture


def capture_image(saveAs):
    #camera.capture(os.path.join("images", "temp", saveAs))
    camera.capture(saveAs)
    #img = cv2.imread(os.path.join("images", "temp", saveAs))
    #hsv_img = cv2.cvtColor(shipsImg, cv2.COLOR_BGR2HSV)
    #return img, hsv_img


def capture_hsv_ranges(saveAs, hsv_masks, iso_val, screen, brightness, screenflip, IMAGE_CAPTURE_DELAY, kernel_size = 3):
    screen.fill((brightness,brightness,brightness))
    screenflip()
    camera.ISO=iso_val
    time.sleep(0.1)
    camera.capture(os.path.join("images", "temp", saveAs))
    camera.ISO=0
    img = cv2.imread(os.path.join("images", "temp", saveAs))
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_loc_names = []
    kernel = np.ones((kernel_size,kernel_size),np.uint8)
    for c , x in enumerate(hsv_masks):
        mask = cv2.inRange(hsv_img, x[0], x[1])
        #mask.save('mask' + str(c) + '.jpg')
        cv2.imwrite(os.path.join("images", "temp", "mask" + str(c) + ".jpg") , mask)
        #erode-dilate this image and save
        erodedDilated = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cv2.imwrite(os.path.join("images", "temp", "mask" + str(c) + "_eroded.jpg") , erodedDilated)
        #create list of mask location names
        mask_loc_names.append(os.path.join("images", "temp", 'mask' + str(c) + '_eroded.jpg'))
    return mask_loc_names

