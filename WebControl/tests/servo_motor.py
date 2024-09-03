#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"
try:
    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(0))
    print("Positionné à 0°")
    time.sleep(1)
    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(90))
    print("Positionné à 90°")
    time.sleep(1)
    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(120))
    print("Positionné à 120°")
    time.sleep(1)
    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(0))
    print("Positionné à 0°")
    time.sleep(1)
    status = "movement successful"
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
except Exception as e:
    print(f"Erreur lors de l'exécution: {e}")
    status = "error"
finally:
    Ab.PWMSERVO.stop() 
    Ab.cleanup()

# Vérification finale et affichage du statut
if status == "movement successful":
    print("Le composant fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)