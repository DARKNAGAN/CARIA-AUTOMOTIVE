#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time, sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization" 
DURATION_LIMIT = 5

try:
    start_time = time.time()  # Enregistrer l'heure de début
    try:
        while time.time() - start_time < DURATION_LIMIT:
            if GPIO.input(Ab.OBSTACLE_PIN) == GPIO.LOW:
                print("Obstacle détecté")
                GPIO.output(Ab.RED_LIGHT, GPIO.HIGH)
                status = "obstacle detected"
            else:
                print("Aucun obstacle détecté")
                GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
                status = "no obstacle detected"
            time.sleep(0.5)  # Attendre un peu entre les lectures pour éviter les faux positifs
    except Exception as e:
        print(f"Erreur pendant l'exécution: {e}")
        status = "erreur"    
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
finally:
    GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
    Ab.cleanup()

# Vérification finale et affichage du statut
if status in ["obstacle detected", "no obstacle detected"]:
    print("Le composant fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)