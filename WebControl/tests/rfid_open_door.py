#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, sys
sys.path.append('/home/christian/WebControl/modules/')
from SimpleMFRC522 import SimpleMFRC522
RFID_MODULE = SimpleMFRC522()
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"
fonctionnement_ok = False

# Lecture initiale du tag RFID
try:   
    print("La porte est actuellement fermée.\nVeuillez approcher votre badge RFID du capteur pour accéder au véhicule.")
    id_rfid, text_rfid = RFID_MODULE.read()
    if text_rfid in ["CHRIS                                           "]:
        Ab.set_angle(90)
        print(f"Salut {text_rfid.rstrip()}, votre accès est validé avec succès.\nLa porte du véhicule est maintenant ouverte!")
        status = "Access successful"
    elif text_rfid == "TEST RFID                                       ":
        Ab.set_angle(90)
        print(f"Bienvenue, {text_rfid.rstrip()}.\nLa porte du véhicule est maintenant ouverte!")
        status = "Access successful"
    else:
        print("Bonjour, vous n'êtes pas autorisé à entrer dans le véhicule.\nLa porte reste fermée.")
        status = "Access denied"
        print(f"(ID, Text)",id_rfid, text_rfid)
        time.sleep(2)
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
except Exception as e:
    print(f"Erreur lors de l'exécution: {e}")
    status = "error"
finally:
    Ab.PWMSERVO.stop() 
time.sleep(2)

# Vérification finale et affichage du statut
if status == "Access successful":
    print("Le composant fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)