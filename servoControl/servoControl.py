
from gpiozero import LED
from gpiozero import AngularServo 
from time import sleep

minAngle = -90
maxAngle = 90
horizontalServo = AngularServo(17, minAngle, maxAngle)
verticalServo = AngularServo(27, minAngle, maxAngle)

while True:
     horizontalServo.angle = -90
     sleep(2)
     horizontalServo.angle = -45
     sleep(2)
     horizontalServo.angle = 0
     sleep(2)
     horizontalServo.angle = 45
     sleep(2)
     horizontalServo.angle = 90
     sleep(2)
     verticalServo.angle = -90
     sleep(2)
     verticalServo.angle = -45
     sleep(2)
     verticalServo.angle = 0
     sleep(2)
     verticalServo.angle = 45
     sleep(2)