// Detecting a pink Aibo ball
// Copyright 2009 mechomaniac.com
 
#include "opencv/cvaux.h"
#include "opencv/highgui.h"
#include "opencv/cxcore.h"
#include <stdio.h>
 
int main(int argc, char* argv[])
{
    CvCapture* camera = cvCreateCameraCapture(-1); // Use the default camera
 
    IplImage* frame = 0;
    CvMemStorage* storage = cvCreateMemStorage(0); //needed for Hough circles
 
    // capturing some extra frames seems to help stability
    frame = cvQueryFrame(camera);
    frame = cvQueryFrame(camera);
    frame = cvQueryFrame(camera);
 
    // with default driver, PSEye is 640 x 480
    CvSize size = cvSize(640,480);
    IplImage *  hsv_frame    = cvCreateImage(size, IPL_DEPTH_8U, 3);
    IplImage*  thresholded    = cvCreateImage(size, IPL_DEPTH_8U, 1);
    IplImage*  thresholded2    = cvCreateImage(size, IPL_DEPTH_8U, 1);
 
    CvScalar hsv_min = cvScalar(0, 50, 170, 0);
    CvScalar hsv_max = cvScalar(10, 180, 256, 0);
    CvScalar hsv_min2 = cvScalar(170, 50, 170, 0);
    CvScalar hsv_max2 = cvScalar(256, 180, 256, 0);
 
    //do {
        frame = cvQueryFrame(camera);
        if (frame != NULL) {
            printf("got frame\n\r");
            // color detection using HSV
            cvCvtColor(frame, hsv_frame, CV_BGR2HSV);
            // to handle color wrap-around, two halves are detected and combined
            cvInRangeS(hsv_frame, hsv_min, hsv_max, thresholded);
            cvInRangeS(hsv_frame, hsv_min2, hsv_max2, thresholded2);
            cvOr(thresholded, thresholded2, thresholded);
 
            cvSaveImage("thresholded.jpg",thresholded);
 
            // hough detector works better with some smoothing of the image
            cvSmooth( thresholded, thresholded, CV_GAUSSIAN, 9, 9 );
            CvSeq* circles = cvHoughCircles(thresholded, storage, CV_HOUGH_GRADIENT, 2, thresholded->height/4, 100, 40, 20, 200);
 
                    for (int i = 0; i < circles->total; i++)
                    {
                        float* p = (float*)cvGetSeqElem( circles, i );
                        printf("Ball! x=%f y=%f r=%f\n\r",p[0],p[1],p[2] );
                            cvCircle( frame, cvPoint(cvRound(p[0]),cvRound(p[1])),
                                             3, CV_RGB(0,255,0), -1, 8, 0 );
                            cvCircle( frame, cvPoint(cvRound(p[0]),cvRound(p[1])),
                                             cvRound(p[2]), CV_RGB(255,0,0), 3, 8, 0 );
                     }
 
            cvSaveImage("frame.jpg", frame);
        } else {
            printf("Null frame\n\r");
        }
  //} while (true);
  cvReleaseCapture(&camera);
  return 0;
}
