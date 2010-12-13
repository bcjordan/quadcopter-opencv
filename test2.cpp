//include files

#include "cv.h"

#include "highgui.h"

#include "math.h"

#include <iostream>

#include <stdio.h>

#include <math.h>

#include <string.h>

#include <conio.h>



using namespace std;

/*==========================================*/

//declarations

int thresh = 50;

IplImage* img = 0;

IplImage* img0 = 0;

CvMemStorage* fstorage = 0;

/*==========================================*/

//main function start

int main (int argc, char** argv ){

        int c;

        int px[0], py[0];

        int edge_thresh = 1;

        IplImage *src = 0; IplImage *csrc;

        IplImage *gray = cvCreateImage( cvSize(320,240), 8, 1 );

        IplImage *edge = cvCreateImage( cvSize(320,240), 8, 1 );

        CvMemStorage* cstorage = cvCreateMemStorage(0);

        fstorage= cvCreateMemStorage(0);

        /*=========================*/

        //get the video from webcam

        CvCapture* capture=cvCaptureFromCAM(0);

        cvNamedWindow("csrc",1);

        cvNamedWindow("src",1);

        /*=========================*/

        //loop start here

        for(;;){

                src=cvQueryFrame(capture);

                csrc=cvCloneImage(src);

                //convert video image color

                cvCvtColor(src,gray,CV_BGR2GRAY);

                //set the converted image's origin

                gray->origin=1;

                //color threshold

                cvThreshold(gray,gray,100,255,CV_THRESH_BINARY);

                //smooth the image to reduce unneccesary results

                cvSmooth( gray, gray, CV_GAUSSIAN, 11, 11 );

                //get edges

                cvCanny(gray, edge, (float)edge_thresh, (float)edge_thresh*3, 5);

                //get circles

                CvSeq* circles =  cvHoughCircles( gray, cstorage, CV_HOUGH_GRADIENT, 2, gray->height/50, 5, 35 );

                //output all the circle detected

                cout << circles->total <<endl;

                //start drawing all the circles

                int i;

                for( i = 0; circles->total>=2?i<2:i < circles->total; i++ ){ //just make a filter to limit only <=2 ciecles to draw

                     float* p = (float*)cvGetSeqElem( circles, i );

                     cvCircle( src, cvPoint(cvRound(p[0]),cvRound(p[1])), 3, CV_RGB(255,0,0), -1, 8, 0 );

                     cvCircle( src, cvPoint(cvRound(p[0]),cvRound(p[1])), cvRound(p[2]), CV_RGB(200,0,0), 1, 8, 0 );

                     px[i]=cvRound(p[0]); py[i]=cvRound(p[1]);

                }

                //output two circles' center position

                cout <<"px0="<<px[0]<<" / px1="<<px[1]<<endl;

                cout <<"py0="<<py[0]<<" / py1="<<py[1]<<endl;

                //start drawing a rectangle between circles detected

                cvRectangle( src, cvPoint(px[0],py[0]), cvPoint(px[1],py[1]), cvScalar( (0), (0), (201) ), -1, CV_AA, 0 );

                //get the space between circles displaying in now window

                if(circles->total>=2) {

                    cvSetImageROI(csrc,cvRect(px[0]>px[1]?px[1]:px[0],py[0]>py[1]?py[1]:py[0],abs(px[0]-px[1]+1),abs(py[0]-py[1]+1)));

                }else{

                    cvSetImageROI(csrc,cvRect(0,0,src->width,src->height));

                };

                cvShowImage("csrc",csrc);

                cvShowImage("src",src);

                //release memory

                cvReleaseImage(&csrc);

                cvClearMemStorage( fstorage );

                //ready to exit loop

                c=cvWaitKey(10);

                if(c==27)break;

        }

        /*=========================*/

        //release video capture

        cvReleaseCapture( &capture);

        //release all windows

        cvDestroyAllWindows();

}

