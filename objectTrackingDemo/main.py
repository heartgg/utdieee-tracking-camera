
<<<<<<< HEAD
from __future__ import print_function

#import videoStreamClass.py
from imutils.video import webcamvideostream
import datetime
import cv2
import time
from threading import Thread

class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.success, self.img) = self.stream.read()
        self.stopped = False
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):

        Thread(target=self.update, args=()).start()
        return self

    def update(self):

        while True:

            if self.stopped:
                return

            (self.success, self.img) = self.stream.read()

            #return self.success

    def read(self):
        return self.img

    def stop(self):
        self.stopped = True

def main():

    # from imutils import FPS
    # from imutils import WebcamVideoStream

    cap = WebcamVideoStream()
    cap.start()
    img = cap.read()
    # defines a webcam object
    # index specifies camera to operate. 0 in this case uses my webcam

    # Initialize tracker \
    #tracker = cv2.legacy.TrackerCSRT_create()
    #tracker = cv2.TrackerCSRT_create()
    tracker = cv2.TrackerMIL_create()

    # success, img = cap.read()  # (self.grabbed, self.frame) = self.stream.read()
    boundingBox = cv2.selectROI("Tracking", img, True, False)

    # Initialize tracker with bounding box
    tracker.init(img, boundingBox)
    ##### TRACKER STUFF FINISHED /

    # verify camera opened
    """if not cap.update.isOpened():  # isOpened() returns a T/F value depending on success of camera opening
        print("Cannot open camera")
        exit()"""

    prevFrameTime = 0
    newFrameTime = 0


    def drawBox(img, boundingBox):
        x, y, w, h = int(boundingBox[0]), int(boundingBox[1]), int(boundingBox[2]), int(boundingBox[3])
        cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)

        # Calculate center coordinates

        centerX = int(x + (w / 2))
        centerY = int(y + (h / 2))
        cv2.circle(img, (centerX, centerY), 5, (255, 0, 255), -1)
        print("X:", str(centerX), "Y:", str(centerY))

        cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)


    def readLoop(prevFrameTime, newFrameTime):
        #### MAKE FUNCTION (SHOULD BE THREAD FOR READING)
        while True:

            img = cap.read()
            boxSuccess, boundingBox = tracker.update(img)  # Updates the bounding box
            # print(boundingBox)

            if boxSuccess:
                drawBox(img, boundingBox)
            else:
                cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

            # Calculates FPS
            newFrameTime = time.time()
            fps = 1 / (newFrameTime - prevFrameTime)
            prevFrameTime = newFrameTime

            # displays formatting on video feed
            cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Tracking", img)

            # If q key has been pressed, stop program
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        ##### MAKE FUNCTION


    Thread(target=readLoop(prevFrameTime, newFrameTime), args=()).start()

    readLoop(prevFrameTime, newFrameTime)

    # release the capture
    cap.stop()

main()
=======
import cv2
import time
from imutils.video import FPS
from imutils.video import WebcamVideoStream

import RPi.GPIO as GPIO


# This function draws a bounding box around the targeted area, calculating its center coordinates
# and drawing a vertical and horizontal axes through the center.
def drawBox(img, boundingBox):
    x, y, w, h = int(boundingBox[0]), int(boundingBox[1]), int(boundingBox[2]), int(boundingBox[3])
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255, 0, 255), 3, 1)

    #Calculate center coordinates
    centerX = int(x + (w/2))
    centerY = int(y + (h/2))
    cv2.circle(img, (centerX, centerY), 5, (255, 0, 255), -1)


    cv2.line(img, (0, centerY), (640, centerY), 5)
    cv2.line(img, (centerX, 0), (centerX, 640), 5)


    #print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)



if __name__ == '__main__':

    # Define camera object and start the stream
    cap = WebcamVideoStream(src=0)
    cap.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    cap.stream.set(cv2.CAP_PROP_FPS,30)
    cap.start()

    # Define fps object and run it
    fps = FPS()
    fps.start()

    # Capture the first frame
    img = cap.read()

    # Initialize tracker
    tracker = cv2.legacy.TrackerMOSSE_create()

    boundingBox = cv2.selectROI("Tracking", img, True)

    # Initialize tracker with bounding box
    tracker.init(img, boundingBox)

    # Initialize initial frame time to 0.
    newFrameTime = 0
    prevFrameTime = 0


    while True:

        img = cap.read()

        boxSuccess, boundingBox = tracker.update(img) # Updates the bounding box
        #print(boundingBox)


        if boxSuccess:
            drawBox(img, boundingBox)
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


        # Calculates FPS
        newFrameTime = time.time()
        framesPerSecond = 1/ (newFrameTime - prevFrameTime)
        prevFrameTime = newFrameTime

        # Update frames
        fps.update()

        # displays formatting on video feed
        cv2.putText(img, str(int(framesPerSecond)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Tracking", img)

        # If q key has been pressed, stop program
        if cv2.waitKey(1) & 0xff == ord('q'):
            fps.stop()
            cap.stop()

            break


    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # Clean up processes
    cv2.destroyAllWindows()

>>>>>>> 6aec1cfaca0b0a6f873fd340ec5773945b432468
