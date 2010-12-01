import cv
import time

cv.NamedWindow("camera", 1)

capture = cv.CaptureFromCAM(0)
print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)

while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    if cv.WaitKey(10) == 27:
        break
    time.sleep(.06)
