#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# Définir la broche GPIO pour le signal du servo-moteur
SERVO_PIN = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

def set_angle(angle):
    pwm = GPIO.PWM(SERVO_PIN, 50)  # Fréquence PWM de 50 Hz
    pwm.start(2.5)  # Position neutre (angle de 0 degrés)
    duty_cycle = angle / 18.0 + 2.5  # Convertir l'angle en devoir (duty cycle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Attendre que le servo atteigne la position désirée
    pwm.stop()

if __name__ == '__main__':
    try:
        setup()
        while True:
            # Faire tourner le servo-moteur de 0 à 180 degrés avec un pas de 30 degrés
            for angle in range(0, 181, 30):
                print("Rotation du servo moteur à {} degrés".format(angle))
                set_angle(angle)
                time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
