
import cv2
import time
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from imutils.video import VideoStream 

# Define camera object and start the stream
#cap = WebcamVideoStream()

cap = VideoStream(src=0, usePiCamera=False, resolution=(640, 480))
cap.start()


# Define fps object and run it
fps = FPS()
fps.start()


while True: 
	img = cap.read()

	# Update frames
	fps.update()

	# displays video feed
	cv2.imshow("Running", img)

	# If q key has been pressed, stop program
	if cv2.waitKey(1) & 0xff == ord('q'):
		break
	
fps.stop()
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Clean up processes
cv2.destroyAllWindows()
cap.stop()
