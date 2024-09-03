#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
sys.path.append('/home/christian/WebControl/modules/')
from SimpleMFRC522 import SimpleMFRC522
RFID_MODULE = SimpleMFRC522()
from AlphaBot import AlphaBot
Ab = AlphaBot()

try:
    # Lecture initiale du tag RFID
    print("### Lecture RFID ###")
    print("Approchez le tag RFID du capteur:")
    print("(ID, Contenu)", RFID_MODULE.read())
    time.sleep(3)
    # Écriture sur le tag RFID
    data = "TEST RFID                                       "
    print("### Écriture RFID ###")
    print("Valeur qui sera écrite:", data)
    print("Approchez le tag RFID du capteur:")
    RFID_MODULE.write(data)
    print("Succès de l'écriture sur le tag RFID.")
    time.sleep(3)  # Attente courte avant de vérifier l'écriture
    # Seconde lecture du tag RFID
    print("### Lecture RFID ###")
    print("Approchez le tag RFID du capteur:")
    print("(ID, Contenu)", RFID_MODULE.read())
    time.sleep(3)
except Exception as e:
    print(f"Erreur lors de l'écriture RFID: {e}")