#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot

Ab = AlphaBot()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
Ab.stop()
speed=100
try:
	while True:

		DR_status = GPIO.input(DR)
		DL_status = GPIO.input(DL)
		if((DL_status == 0) and (DR_status == 0)):
			Ab.forward(speed)
		elif((DL_status == 1) and (DR_status == 0)):
			Ab.right(speed)
		elif((DL_status == 0) and (DR_status == 1)):
			Ab.left(speed)
		else:
			Ab.stop()
except KeyboardInterrupt:
	GPIO.cleanup();

