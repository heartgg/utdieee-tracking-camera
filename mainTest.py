
import cv2
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Pin definitions
pan = 18
tilt = 17


# Base duty  cycle angles 
panDC = 90
tiltDC = 90 


# assign GPIO pins to PWM channels
GPIO.setup(pan, GPIO.OUT)
GPIO.setup(tilt, GPIO.OUT)

panPWM = GPIO.PWM(pan,50)
tiltPWM = GPIO.PWM(tilt,50)


#def translateToDC(servoPWM, angle):
    #servoPWM.ChangeDutyCycle(5. + angle / 36.)
    #sleep(0.5)
	
        

    

        
def computeServoResponse(x, y, originX, originY):

    # X is the face center x-coordinate
    # Y is the face center y-coordinate
    
    # originX is the frame center x-coordinate
    # originY is the frame center y-coordinate
    
    global panDC
    global tiltDC
    
    
    # Debugging 
    print("PanDC: ", panDC)
    print("tiltDC: ", tiltDC)
    
 
    
    if (x < originX + 40): # if x coordinate of center is 40 from x-center of frame, move pan right
        panDC += 20
        if panDC > 150:
            panDC = 180
        panPWM.ChangeDutyCycle(5. + panDC / 36.)
        
    if(x > originX - 40): # if x coordinate of center is -40 from x-center of frame, move pan left
        panDC -= 20
        if panDC < 30:
            panDC = 0
        panPWM.ChangeDutyCycle(5. + panDC / 36.)

    if (y > originY + 40): # if y coordinate is +40 from y-center of frame, move tilt up
        tiltDC += 20
        if tiltDC > 150:
            tiltDC = 180
        tiltPWM.ChangeDutyCycle(5. + tiltDC / 36.)
    if(y < originY - 40): # if y coordinate is -40 from y-center of frame, move tilt down
        tiltDC -= 20
        if tiltDC < 30:
            tiltDC = 0
        tiltPWM.ChangeDutyCycle(5. + tiltDC / 36.)
    
        
    


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
    #print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    computeServoResponse(centerX, centerY, frameCenterX, frameCenterY)

if __name__ == '__main__':
    
   
    #Define camera object and start the stream
    cap = cv2.VideoCapture(-1); 
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS,30)
    
    
    # Set servos to 90 degrees initiallity 
    panPWM.start(7.5)
    tiltPWM.start(7.5) 


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
        img = cv2.resize(img, (640, 480)) 
        #time.sleep(1)
        
    
        boxSuccess, boundingBox = tracker.update(img) # Updates the bounding box
        #print(boundingBox)


        if boxSuccess:
           drawBox(img, boundingBox)
           time.sleep(0.1)
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


        # Calculates FPS
        newFrameTime = time.time()
        framesPerSecond = 1/ (newFrameTime - prevFrameTime)
        prevFrameTime = newFrameTime


        # displays formatting on video feed
        cv2.putText(img, str(int(framesPerSecond)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Tracking", img)

        # If q key has been pressed, stop program
        if cv2.waitKey(1) & 0xff == ord('q'):
            #fps.stop()
            break



    # Clean up processes
    cv2.destroyAllWindows()
    GPIO.cleanup()
