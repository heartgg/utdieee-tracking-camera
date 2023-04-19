# import threading package
from threading import Thread
import cv2

class WebcamVideoStream:
    def __init__(self, src=0):
        # Constructor initializes the video camera stream
        # and reads the first frame from the stream

        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread
        # should be stopped
        self.stopped = False

    def start(self):
        # This starts the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # This keeps looping infinitely until the threat is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the threat should be stopped
        self.stopped = True
