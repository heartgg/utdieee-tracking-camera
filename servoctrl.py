import RPi.GPIO as GPIO
from time import sleep
GPIO.setMode(BCM) //not on-board numbered pins, the numbers beside GPIO to reference pins

GPIO.setwarnings(False)


servo = 18 // GPIO 18
GPIO.setOutput(servo, GPIO.OUT)
pwm = GPIO.PWM(servo, 50) setting PWM for GPIO 18 at 50kHz (servo frequency)
pwm.start(7) // neutral servo position duty cycle

servo.ChangeDutyCycle(2)
sleep(0.5)
servo.changeDutyCycle(7)
sleep(0.5)
servo.changeDutyCycle(12)
sleep(0.5)

servo = stop()
GPIO.cleanup()

