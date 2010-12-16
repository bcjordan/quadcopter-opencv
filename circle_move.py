# Quadrotor vision code
# Usage: redirect standard error to the file "geterrors" like so:
#        python circle_move.py 2> geterrors
# Finds serial consoles and cameras as they are attached (serial first)
# 
# By Brian Jordan for COMP150 Behavior Based Robotics
#   Used API at http://opencv.willowgarage.com/wiki/SwigPythonInterface 
#   and circle detection tutorials at http://mechomaniac.com/robots 
#   for reference.


from opencv.cv import *
from opencv.highgui import *
import serial
import os
import time

DEBUG = False
CAMERA = True
VERBOSE_DEBUG = False
CSV = True
CLEAN_FRAMES = False

# Check for serial connection, try and catch errors, try new card 

while True:
    try:
        copter = serial.Serial('/dev/tty-serial.*', 9600, timeout = 5)
    except:
        time.sleep(5)

# If we are currently 
if CAMERA: cvStartWindowThread()
if CAMERA: cvNamedWindow("camera")

# Helper functions
def serial(orientation, direction):
    copter.write("#M" + orientation + direction + "#")

def average(values):
    """ Compute mean of values in a list of numbers. """
    if len(values) == 0:
        return None
    else:
        return sum(values,0.0) / len(values)


# Generate frame storage image areas using OpenCV API
size = cvSize(640, 480)
hsv = cvCreateImage(size, IPL_DEPTH_8U, 3)
thresholded = cvCreateImage(size, IPL_DEPTH_8U, 1)
thresholded2 = cvCreateImage(size, IPL_DEPTH_8U, 1)

# Because the hue of red wraps around the 256/0 barrier, we define two min/maxes
# for our color matching.

# Define red low hue upper and lower bounds 
hsv_min = cvScalar(0, 40, 160, 0)
hsv_max = cvScalar(10, 170, 256, 0)

# Define red high hue upper and lower bounds
hsv_min2 = cvScalar(160, 40, 160, 0)
hsv_max2 = cvScalar(256, 170, 256, 0)

# Allocate storage space for current frame and operations 
storage = cvCreateMemStorage(0)

# Initialize camera capture
while True:
    try:
        capture = cvCreateCameraCapture(0)
        if capture:
            break
        else:
            time.sleep(5) # Wait 5 seconds for next attempt
    except:
        time.sleep(5)

# Set capture variables (still not implemented in either OpenCV API)
# cvSetCaptureProperty(capture, CV_CAP_PROP_FPS, 20) 

# Read size of our error file. This is a hacky solution to bad frames caused
# by unresolvable v4l jpeg decompression bugs. When this is run with the option 2> geterrors,
# we can detect changes in the file size of geterrors and know we have just been
# given a corrupt jpeg frame, so we do not process it as important data.
last_errors = os.path.getsize("geterrors")

# Run our main webcam capture, circle finding, and serial out loop
while True:
    # Grab the current frame from our webcam capture
    frame = cvQueryFrame(capture)

    # Check cleanliness of frame. If capture threw a jpeg corruption error,
    # throw our frame out.
    if(os.path.getsize("geterrors") > last_errors):
        if VERBOSE_DEBUG: print "More errors!"
        last_errors = os.path.getsize("geterrors")   # Update last error file size
        if CLEAN_FRAMES: frame = None

    if frame is not None:    
        # If we have a clean frame to work with        
        # Show our image in the GUI if we are debugging
        if CAMERA: cvShowImage("camera", frame)
        # cvSaveImage("test.jpg", frame)

        # Convert frame to HSV color format for color matching
        # because hue wraps around, we need to match it in 2 parts and OR together
        cvCvtColor(frame, hsv_frame, CV_BGR2HSV)
        cvInRangeS(hsv_frame, hsv_min, hsv_max, thresholded)
        cvInRangeS(hsv_frame, hsv_min2, hsv_max2, thresholded2)
        cvOr(thresholded, thresholded2, thresholded)
 
        # Smoothing improves Hough detector
        cvSmooth(thresholded, thresholded, CV_GAUSSIAN, 9, 9)

        # Run HoughCircle detector. Calculates gradient and returns unique separated circles
        # Arguments are: image, storage, hough method, accumulator resolution
        # (bigger is smaller), minimum distance btwn circles, hough canny
        # edge detector threshold, center detection threshold (higher =
        # larger circles only), minimum radius of circles, maximum radius
        # of circles.
        circles = cvHoughCircles(thresholded, storage, CV_HOUGH_GRADIENT, 2, thresholded.height/4, 100, 40, 20, 200)
 
        # Analyze found circles array. Find best (in this case, largest) circle.
        radius = x = y = 0

        # Store last 5 xs and ys for sudden change analysis
        last_xs = []
        last_ys = []

        x = none 
       
        # Radius is best radius found, x is best x fond, y is best y found 
        for circle in circles:
            if circle[2] > radius:
                radius = circle[2]
                x = circle[0]
                y = circle[1]
 
        if found: # If we have detected a ball

            if DEBUG: print "ball detected at position:",x,",",y," with radius ", maxRadius
            if CSV: print x, ",", y, ",", maxRadius, ",", circles.total, ",", time.time()

            if len(last_xs) == 5: del last_xs[0] # Remove first item
            last_xs.append(x)
            if len(last_ys) == 5: del last_ys[0] # Remove first item
            last_ys.append(y)
 
            if abs(average(last_xs)-x) > 40: # Then x is probably a bad measurement 
                x = average(last_xs)
                if DEBUG: print "ball fixed:",x,",",y
            if abs(average(last_ys)-y) > 40: # Then y is probably a bad measurement 
                y = average(last_ys)
                if DEBUG: print "ball fixed:",x,",",y
            

            # Communicate commands or location via serial cable
            if x > 320:
                # Copter must move right
               serial("ROLL","RIGHT")
            elif x < 320:
               serial("ROLL","LEFT")

            if y > 240:
                # Copter must move backwards 
               serial("PITCH","FORWARD")
            elif y < 240:
               serial("PITCH","BACK")

copter.close()
# Stop taking frames from camera
