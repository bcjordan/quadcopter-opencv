from opencv.cv import *
from opencv.highgui import *
size = cvSize(640, 480)
hsv_frame = cvCreateImage(size, IPL_DEPTH_8U, 3)
storage = cvCreateMemStorage(0)
capture = cvCreateCameraCapture(0)
frame = cvQueryFrame(capture)
cvSaveImage("test_save_frame.jpg", frame)
