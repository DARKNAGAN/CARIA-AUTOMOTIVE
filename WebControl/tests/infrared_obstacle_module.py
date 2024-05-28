#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

ObstaclePin = 16

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ObstaclePin, GPIO.IN)

def loop():
    while True:
        if GPIO.input(ObstaclePin) == GPIO.LOW:
            print("Obstacle détecté")
        else:
            print("Aucun obstacle détecté")
        time.sleep(0.5)  # Attendre un peu entre les lectures pour éviter les faux positifs

        
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
