import RPi.GPIO as GPIO
from time import sleep

# this program converts desired servo angle movement to duty cycle

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tilt = 17
pan = 18

GPIO.setup(tilt, GPIO.OUT)
GPIO.setup(pan, GPIO.OUT)

def translateToDC(servoPin, angle):
	servoPWM = GPIO.PWM(servoPin,50)
	servoPWM.start(7.5) # reposition to center/default
	servoPWM.ChangeDutyCycle(5. + angle / 36.)
	sleep(0.5)
	servoPWM.stop()

while True:
	for angle in range (0, 180, 20):
		translateToDC(tilt, angle)
		translateToDC(pan, angle)
		sleep(0.5)
	for angle in range(180, 0, -20):
		translateToDC(tilt, angle)
		translateToDC(pan, angle)
		sleep(0.5)


GPIO.cleanup()
	