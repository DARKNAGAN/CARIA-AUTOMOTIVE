#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, time, sys
sys.path.append('/home/christian/WebControl/modules/')
from SimpleMFRC522 import SimpleMFRC522
RFID_MODULE = SimpleMFRC522()
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"
try:
    while True:
        Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(0))
        time.sleep(1)
        print("La porte est actuellement fermée.\nVeuillez approcher votre badge RFID du capteur pour accéder au véhicule.")
        id_rfid, text_rfid = RFID_MODULE.read()
        rfid_content = RFID_MODULE.read()
        if text_rfid == "TEST RFID                                       ":
            Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(90))
            time.sleep(1)
            print(f"Bienvenue, {text_rfid.rstrip()} \nJe suis heureux de pouvoir partager un trajet avec vous !")
            time.sleep(5)
            print("Installez-vous confortablement !")
            time.sleep(2)
            print("Votre voiture autonome est prête à partir.")
            try:
                subprocess.run(['python3', 'apps/itineraire_create.py'], check=True)
                try:
                    print("Nous préparons votre trajet en toute sécurité.")
                    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(0))
                    time.sleep(1)
                    # Changer si nécessaire 'apps/itineraire_suivre.py' en 'apps/itineraire_suivre_emergency.py'
                    subprocess.run(['python3', 'apps/itineraire_suivre.py'], check=True)
                    print("Merci d'avoir utilisé notre service !")
                    Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(90))
                    time.sleep(2)
                    print("Nous espérons que vous avez apprécié votre trajet.")
                    time.sleep(2)
                    print("À bientôt avec CARIA !")
                    status = "scenario successful"
                except subprocess.CalledProcessError as e:
                    print(f"Erreur lors de l'exécution du script step2_suivre_itineraire: {e}")
                    status = "error"
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution  du script step1_prepare_itineraire: {e}")
                status = "error"
        elif text_rfid in ["CHRIS                                           "]:
            Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(90))
            time.sleep(1)
            print(f"Bienvenue, {text_rfid.rstrip()}.\nLa porte du véhicule est maintenant ouverte!")
            status = "scenario successful"
        else:
            Ab.PWMSERVO.ChangeDutyCycle(Ab.set_angle(0))
            print("Bonjour, vous n'êtes pas autorisé à entrer dans le véhicule.\nLa porte reste fermée.")
            print(rfid_content)
            time.sleep(2)
            status = "interrupted"
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
        print("Le scenario fonctionne correctement.")
        fonctionnement_ok = True
    else:
        print(f"Le scenario a rencontré un problème: {status}.")
        fonctionnement_ok = False
Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)
