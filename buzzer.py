import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)


while True:
	GPIO.output(16, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(16, GPIO.LOW)
	print("sonando")

GPIO.cleanup()
