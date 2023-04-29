import cv2
import time 






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

    




if __name__ == '__main__':
    

    

    cap = cv2.VideoCapture(-1); 

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS,30)
    
    
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

     

        # displays formatting on video feed
        cv2.putText(img, str(int(framesPerSecond)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Tracking", img)

        # If q key has been pressed, stop program
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


       

    # Clean up processes
    cv2.destroyAllWindows()