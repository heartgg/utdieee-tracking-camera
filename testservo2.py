import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


tiltServo = 17
panServo = 18 
GPIO.setup(tiltServo, GPIO.OUT)
GPIO.setup(panServo, GPIO.OUT)
pwm1 = GPIO.PWM(tiltServo, 50) 
pwm1.start(7)
pwm2 = GPIO.PWM(panServo, 50) 
pwm2.start(7)

while True:
	for dc in range (2, 12):
		pwm1.ChangeDutyCycle(dc)
		pwm2.ChangeDutyCycle(dc)
		sleep(0.5)
		
	for dc in range (12, 2,-1):
		pwm1.ChangeDutyCycle(dc)
		pwm2.ChangeDutyCycle(dc)
		sleep(0.5)




GPIO.cleanup()
