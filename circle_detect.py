from opencv.cv import *
from opencv.highgui import *
size = cvSize(640, 480)

hsv_frame = cvCreateImage(size, IPL_DEPTH_8U, 3)
thresholded = cvCreateImage(size, IPL_DEPTH_8U, 1)
thresholded2 = cvCreateImage(size, IPL_DEPTH_8U, 1)
hsv_min = cvScalar(0, 50, 170, 0)
hsv_max = cvScalar(10, 180, 256, 0)
hsv_min2 = cvScalar(170, 50, 170, 0)
hsv_max2 = cvScalar(256, 180, 256, 0)
storage = cvCreateMemStorage(0)
capture = cvCreateCameraCapture(0)
frame = cvQueryFrame(capture)
cvSaveImage("test.jpg", frame)

# Convert to HSV for color matching
cvCvtColor(frame, hsv_frame, CV_BGR2HSV)
cvInRangeS(hsv_frame, hsv_min, hsv_max, thresholded)
cvInRangeS(hsv_frame, hsv_min2, hsv_max2, thresholded2)
cvOr(thresholded, thresholded2, thresholded)

# Pre-smoothing
cvSmooth(thresholded, thresholded, CV_GAUSSIAN, 9, 9)

# Hough detector
circles = cvHoughCircles(thresholded, storage, CV_HOUGH_GRADIENT, 2, thresholded.height/4, 100, 40, 20, 200)

maxRadius = 0
x = 0
y = 0
found = False
for i in range(circles.total):
    circle = circles[i]
    if circle[2] > maxRadius:
	found = True
	maxRadius = circle[2]
	x = circle[0]
	y = circle[1]
	
if found:
    print "ball detected at position:",x, ",", y, " with radius:", maxRadius
