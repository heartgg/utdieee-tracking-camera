
import cv2
import time

# defines a webcam object
# index specifies camera to operate. 0 in this case uses my webcam
cap = cv2.VideoCapture(0)


# Initialize tracker
tracker = cv2.legacy.TrackerCSRT_create()

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
    print( "X:", str(centerX), "Y:", str(centerY))

    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

while True:

    readSuccess, img = cap.read()

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


