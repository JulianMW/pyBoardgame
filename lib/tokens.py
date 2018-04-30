# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1) # allow the camera to warmup

def captureImage(saveAs):
    camera.capture(os.path.join("images", "temp", saveAs))
    img = cv2.imread(os.path.join("images", "temp", saveAs))
    hsv_img = cv2.cvtColor(shipsImg, cv2.COLOR_BGR2HSV)
    return img, hsv_img

