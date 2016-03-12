import RPi.GPIO as GPIO
import time
import pygame

print "init pygame"
#pygame.init()

GPIO.setmode(GPIO.BCM)
TRIG=23
ECHO=24

print "Distance mesurement in Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)
print "Waiting For Sensor to Settle"
time.sleep(2)

distance = 100000;
while distance > 200:
	GPIO.output(TRIG,True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration*17150
	distance = round(distance, 2)

	print "Distance: ",distance," cm"

	time.sleep(0.2)
	

print "OK distance min atteinte"
pygame.init()
pygame.mixer.music.load("/home/pi/distanceSensor/python/messageMarianne.wav")
pygame.mixer.music.play(1)

time.sleep(40)

GPIO.cleanup()
