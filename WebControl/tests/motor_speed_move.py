#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

# Variable de statut pour indiquer le bon fonctionnement
status = "initialization"
# Test de la classe AlphaBot avec différentes vitesses pour les moteurs individuels

duration = 0.5
try:
    for speed in range(20, 81, 30):
        print(f"Test de vitesse à {speed}%")
        # Test des moteurs en avance
        Ab.forward(duration, speed)
        Ab.stop(1)
        # Test des moteurs en arrière
        Ab.backward(duration, speed)
        Ab.stop(1)
        # Test du moteur gauche en avant et moteur droit en arrière
        Ab.left(duration, speed)
        Ab.stop(1)
        # Test du moteur gauche en arrière et moteur droit en avant
        Ab.right(duration, speed)
        Ab.stop(1)
    status = "move successful"
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
except Exception as e:
    print(f"Erreur lors du test: {e}")
    status = "error"
finally:
    Ab.cleanup()

# Vérification finale et affichage du statut
if status == "move successful":
    print("Le composant fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)