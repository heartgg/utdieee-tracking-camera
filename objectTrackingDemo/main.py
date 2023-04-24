<<<<<<< HEAD:objectTrackingDemo/main.py

import cv2
import time


# user chooses which camera to use
cameraSelect = input("0 for Webcam, 1 for Arducam")
while cameraSelect is not 0 or 1:
    cameraSelect = input("0 for Webcam, 1 for Arducam")

# Define camera object
cap = cv2.VideoCapture()

# selects webcam or camera object
if cameraSelect == 0:
    cap = cv2.VideoCapture(0)
elif cameraSelect == 1:
    cap = cv2.VideoCapture(1)

# Initialize tracker
tracker = cv2.legacy.TrackerKCF_create()

success, img = cap.read()

boundingBox = cv2.selectROI("Tracking", img, True, False)

# Initialize tracker with bounding box
tracker.init(img,boundingBox)



# verify camera opened
if not cap.isOpened(): # isOpened() returns a T/F value depending on success of camera opening
    print("Cannot open camera")
    exit()


prevFrameTime = 0
newFrameTime = 0

def drawBox(img, boundingBox):
    x, y, w, h = int(boundingBox[0]), int(boundingBox[1]), int(boundingBox[2]), int(boundingBox[3])
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255, 0, 255), 3, 1)

    #Calculate center coordinates
    centerX = int(x + (w/2))
    centerY = int(y + (h/2))
    cv2.circle(img, (centerX, centerY), 5, (255, 0, 255), -1)


    cv2.line(img, (0, centerY), (640, centerY), 5)
    cv2.line(img, (centerX, 0), (centerX, 640), 5)


    print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

while True:

    readSuccess, img = cap.read()
    #print(img.shape)

    boxSuccess, boundingBox = tracker.update(img) # Updates the bounding box
    #print(boundingBox)


    if boxSuccess:
        drawBox(img, boundingBox)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


    # Calculates FPS
    newFrameTime = time.time()
    fps = 1/ (newFrameTime - prevFrameTime)
    prevFrameTime = newFrameTime



    # displays formatting on video feed
    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Tracking", img)

    # If q key has been pressed, stop program
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


# release the capture
cap.release()


=======
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
    tracker = cv2.legacy.TrackerCSRT_create()
    tracker = cv2.TrackerCSRT_create()

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
>>>>>>> c2be4fff49bcb8e31fa66c4798ade8dd9aae72d1:main.py
