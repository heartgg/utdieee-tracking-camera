
import cv2
import time
from time import sleep
import pigpio




# Pin definitions
pan = 18
tilt = 17


# Base duty  cycle angles 
panDC = 0
tiltDC = 0 


# Setting up Pins 
panPWM = pigpio.pi()
tiltPWM = pigpio.pi()

panPWM.set_mode(pan, pigpio.OUTPUT) 
tiltPWM.set_mode(tilt, pigpio.OUTPUT)

panPWM.set_PWM_frequency(pan, 50)
tiltPWM.set_PWM_frequency(tilt, 50) 

        
def computeServoResponse(x, y, originX, originY):

    # X is the face center x-coordinate
    # Y is the face center y-coordinate
    
    # originX is the frame center x-coordinate
    # originY is the frame center y-coordinate
    
    global panDC
    global tiltDC
    
    if (x < originX + 60): # if x coordinate of center is 40 from x-center of frame, move pan right
        panDC += 5
        if panDC > 70:
            panDC = 90
        panPWM.set_servo_pulsewidth(pan, ((500/90)* panDC) + 1500)
        
    if(x > originX - 60): # if x coordinate of center is -40 from x-center of frame, move pan left
        panDC -= 5
        if panDC < -70:
            panDC = -90
        panPWM.set_servo_pulsewidth(pan, ((500/90) * panDC) +1500)

    if (y > originY + 60): # if y coordinate is +40 from y-center of frame, move tilt up
        tiltDC += 5
        if tiltDC > 70:
            tiltDC = 90
        tiltPWM.set_servo_pulsewidth(tilt, ((500/90) * tiltDC) + 2000)
    if(y < originY - 60): # if y coordinate is -40 from y-center of frame, move tilt down
        tiltDC -= 5
        if tiltDC < -70:
            tiltDC = -90
        tiltPWM.set_servo_pulsewidth(tilt, ((500/90)* tiltDC) + 2000)
    
    
    # Debugging Info
    #panPulseWidth = panPWM.get_servo_pulsewidth(pan)
    #tiltPulseWidth = panPWM.get_servo_pulsewidth(tilt)
    #print("PanDC: ", panDC)
    #print("tiltDC: ", tiltDC)
    #print("Pan pulsewidth: ", panPulseWidth)
    #print("Tilt pulsewidth: ", tiltPulseWidth)
    
        
        
# This function draws a bounding box around the targeted area, calculating its center coordinates
# and drawing a vertical and horizontal axes through the center.
def drawBox(img, boundingBox):
    x, y, w, h = int(boundingBox[0]), int(boundingBox[1]), int(boundingBox[2]), int(boundingBox[3])
    
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255, 0, 255), 3, 1)


    # Get center coordinates of the image
    frameCenterX, frameCenterY = img.shape[:2]
    frameCenterX = 1/2 * frameCenterX
    frameCenterY = 1/2 * frameCenterY 

    #Calculate center coordinates
    centerX = int(x + (w/2))
    centerY = int(y + (h/2))
    cv2.circle(img, (centerX, centerY), 5, (255, 0, 255), -1)
    #print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    computeServoResponse(centerX, centerY, frameCenterX, frameCenterY)

if __name__ == '__main__':
    
   
    #Define camera object and start the stream
    cap = cv2.VideoCapture(0); 
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS,30)
    

    # Set servos to the center initially 
    panPWM.set_servo_pulsewidth(pan, 1500)
    tiltPWM.set_servo_pulsewidth(tilt, 2000)


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
    
    sleep(1)
    
    while True:
        
     
        ret, img = cap.read()
        img = cv2.resize(img, (640, 480)) 
        
    
        boxSuccess, boundingBox = tracker.update(img) # Updates the bounding box


        if boxSuccess:
           drawBox(img, boundingBox)
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
            break  

    # Clean up processes
    cv2.destroyAllWindows()
    
