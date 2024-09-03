#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time, sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"
duration = 0.1
speed = 20

try:
    start_time = time.time()  # Enregistrer l'heure de début
    while time.time() - start_time < 10:  # Boucle pendant 5 seconde
        OBSTACLE_PIN_status = GPIO.input(Ab.OBSTACLE_PIN)
        if OBSTACLE_PIN_status == 1:
            Ab.forward(duration, speed)
            status = "operation successful"
        else:
            Ab.emergencystop()
            status = "emergency stop successful"
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
finally:
    Ab.cleanup()
# Vérification finale et affichage du statut
if status == "operation successful" or status == "emergency stop successful":
    print(f"Le composant fonctionne correctement: {status}.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)
