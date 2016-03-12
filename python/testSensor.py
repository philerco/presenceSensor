import RPi.GPIO as GPIO
import time
import pygame

sound_file = ""
time_of_sound = 0
distance_max = 0
isplaying = 0
TRIG=23
ECHO=24

def load_param():
	global sound_file
	global time_of_sound
	global distance_max

	f = open("/home/pi/Projects/presenceSensor/conf/config.txt", 'r');
	sound_file = f.readline().rstrip()
	time_of_sound = int(f.readline())
	distance_max = int(f.readline())
	f.close()

def play_music():
	global isplaying

	if isplaying==0:
		print "play music"
		pygame.init()
		print "init ok"
		print sound_file
		pygame.mixer.music.load(sound_file)
		print "play file ok"
		pygame.mixer.music.play(1)
		print "playing"
		isplaying=1

def stop_music():
	global isplaying
	if isplaying==1:
		print "stop music"
		pygame.mixer.music.stop()
		pygame.quit()
		isplaying=0

def get_distance():
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

	return distance

print "init pygame"
#pygame.init()

print "load parameters"
load_param()

GPIO.setmode(GPIO.BCM)

print "Distance mesurement in Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)
print "Waiting For Sensor to Settle"
time.sleep(2)

print "init cptr"
last_time = time.time()

distance = 100000;
while 1:
	distance = get_distance()
	print "Distance: ",distance," cm"

	if(distance > distance_max):
		if isplaying==1:
			timeplaying = time.time() - last_time
			print timeplaying
			print time_of_sound
			if (time.time() - last_time) > time_of_sound:
				stop_music()
	else:
		last_time =  time.time()
		play_music()
		time.sleep(2)

	time.sleep(0.2)	

print "OK distance min atteinte"
pygame.init()
pygame.mixer.music.load("/home/pi/distanceSensor/python/messageMarianne.wav")
pygame.mixer.music.play(1)

time.sleep(40)

GPIO.cleanup()
