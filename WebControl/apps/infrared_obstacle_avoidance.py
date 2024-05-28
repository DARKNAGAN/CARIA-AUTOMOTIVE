#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot

Ab = AlphaBot()
speed = 100
DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
	while True:
		DR_status = GPIO.input(DR)
		DL_status = GPIO.input(DL)
		if((DL_status == 1) and (DR_status == 1)):
			Ab.forward(speed)
		elif((DL_status == 1) and (DR_status == 0)):
			Ab.left(speed)
		elif((DL_status == 0) and (DR_status == 1)):
			Ab.right(speed)
		else:
			Ab.backward(speed)
			time.sleep(0.2)
			Ab.left(speed)
			time.sleep(0.2)
			Ab.stop()

except KeyboardInterrupt:
	GPIO.cleanup();

