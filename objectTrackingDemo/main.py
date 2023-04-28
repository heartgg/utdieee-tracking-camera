
import cv2
import time
from threading import Thread
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from imutils.video import VideoStream 

class VideoShow:
    # Separates imshow() into its own dedicated thread 
    
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self
        
    def show(self): 
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True
                
    def stop(self):
        self.stopped = True 
        




# Define camera object and start the stream
#cap = WebcamVideoStream()
cap = VideoStream(src=0, usePiCamera=False, resolution=(640, 480), framerate=30)
cap.start()

# Define fps object and run it
fps = FPS()
fps.start()

 

# Capture the first frame
img = cap.read()

# Define VideoShow object (takes place of cv2 imshow() )
#videoFeed = VideoShow(img)
#videoFeed.start()


# Initialize tracker
tracker = cv2.legacy.TrackerMOSSE_create()

boundingBox = cv2.selectROI("Tracking", img, True, False)
# Initialize tracker with bounding box
tracker.init(img,boundingBox)


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


newFrameTime = 0
prevFrameTime = 0

resetServo(pan)
resetServo(tilt)

while True:
    
    img = cap.read()
    #print(img.shape)

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
    
    # Non-multithreaded
    cv2.imshow("Tracking", img)
    
    # With multithreading 
    #videoFeed.show() 
    #videoFeed.frame = img

    # If q key has been pressed, stop program
    if cv2.waitKey(1) & 0xff == ord('q'):
        break



fps.stop()
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Clean up processes
cv2.destroyAllWindows()
#videoFeed.stop()
cap.stop()
