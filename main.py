
import cv2
import time
from imutils.video import FPS
from imutils.video import WebcamVideoStream

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pan = 18
tilt = 17




GPIO.setup(pan, GPIO.OUT)
GPIO.setup(tilt, GPIO.OUT)

panPWM = GPIO.PWM(pan,50)
tiltPWM = GPIO.PWM(tilt,50)


def translateToDC(servoPin, angle):
	servoPWM = GPIO.PWM(servoPin, 50)
	servoPWM.ChangeDutyCycle(5. + angle / 36.)
	sleep(0.5)
        

    

        
def computeServoResponse(x, y, originX, originY, panDC, tiltDC):

    # X is the face center x-coordinate
    # Y is the face center y-coordinate
    
    # originX is the frame center x-coordinate
    # originY is the frame center y-coordinate
    
    

    
    if (x < originX - 40):
        panDC += 5.5
        if panDC > 9:
            panDC = 10
        panPWM.ChangeDutyCycle(panDC)
    if(x > originX + 40):
        panDC -= 5.5
        if panDC < 6:
            panDC = 5
        panPWM.ChangeDutyCycle(panDC)

    if(y < originY - 40):
        tiltDC += 5.5
        if tiltDC > 9:
            tiltDC = 10
        tiltPWM.ChangeDutyCycle(tiltDC)
    if(y > originY + 40):
        tiltDC -= 5.5
        if tiltDC < 6:
            tiltDC = 5
        tiltPWM.ChangeDutyCycle(tiltDC)

# This function draws a bounding box around the targeted area, calculating its center coordinates
# and drawing a vertical and horizontal axes through the center.
def drawBox(img, boundingBox):
    x, y, w, h = int(boundingBox[0]), int(boundingBox[1]), int(boundingBox[2]), int(boundingBox[3])
    
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255, 0, 255), 3, 1)

    frameCenterX = 320
    frameCenterY = 240

    #Calculate center coordinates
    centerX = int(x + (w/2))
    centerY = int(y + (h/2))
    cv2.circle(img, (centerX, centerY), 5, (255, 0, 255), -1)
    

    #cv2.line(img, (0, centerY), (640, centerY), 5)
    #cv2.line(img, (centerX, 0), (centerX, 640), 5)


    #print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    computeServoResponse(centerX, centerY, frameCenterX, frameCenterY, 7.5, 7.5)

if __name__ == '__main__':
    
   

    
    #cap.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #cap.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    #cap.stream.set(cv2.CAP_PROP_FPS,30)
    
    #cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    
  
    
    #Define camera object and start the stream
    #cap = WebcamVideoStream(1)
    cap = cv2.VideoCapture(-1); 
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS,30)
    
    #cap.start()
    
    # Define fps object and run it
    #fps = FPS()
    #fps.start()
    
    
    # Capture the first frame
    ret, img = cap.read()
    img = cv2.resize(img, (640, 480))

    # Initialize tracker
    tracker = cv2.legacy.TrackerMOSSE_create()

    boundingBox = cv2.selectROI("Tracking", img, True)

    # Initialize tracker with bounding box
    tracker.init(img, boundingBox)

    # Initialize initial frame time to 0.
    newFrameTime = 0
    prevFrameTime = 0

   
    
    
    while True:
        
     
        ret, img = cap.read()
        img = cv2.resize(img, (640, 480)) #
        #time.sleep(1)
        
    
        boxSuccess, boundingBox = tracker.update(img) # Updates the bounding box
        #print(boundingBox)


        if boxSuccess:
           drawBox(img, boundingBox)
           print("lol")

        
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


        # Calculates FPS
        newFrameTime = time.time()
        framesPerSecond = 1/ (newFrameTime - prevFrameTime)
        prevFrameTime = newFrameTime

        # Update frames
        #fps.update()

        # displays formatting on video feed
        cv2.putText(img, str(int(framesPerSecond)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Tracking", img)

        # If q key has been pressed, stop program
        if cv2.waitKey(1) & 0xff == ord('q'):
            #fps.stop()
            #cap.stop()

            break


        


    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # Clean up processes
    cv2.destroyAllWindows()
    GPIO.cleanup()
