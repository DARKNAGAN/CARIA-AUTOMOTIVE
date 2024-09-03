#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"
try:
    Ab.set_angle(0)
    print("Positionné à 0°")
    time.sleep(2)
    Ab.set_angle(90)
    print("Positionné à 90°")
    time.sleep(2)
    Ab.set_angle(180)
    print("Positionné à 180°")
    time.sleep(2)
    Ab.set_angle(0)
    print("Positionné à 0°")
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