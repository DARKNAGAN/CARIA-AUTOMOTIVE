#!/usr/bin/env python

# Importation des bibliothèques
import time
from gpiozero import LED
from joyit_mfrc522 import SimpleMFRC522

# Initialisation de l'objet pour le module RFID
reader = SimpleMFRC522()

# Fonction pour la lecture du tag RFID
def read_rfid():
    print("### Lecture RFID ###")
    print("Approchez le tag RFID du capteur:")
    id, text = reader.read()
    print("ID:", id)
    print("Contenu:", text)
    time.sleep(5)

# Fonction pour l'écriture sur le tag RFID avec gestion des erreurs
def write_rfid(data, max_attempts=3):
    print("### Écriture RFID ###")
    print("Valeur qui sera écrite:", data)
    print("Approchez le tag RFID du capteur:")
    try:
        reader.write(data)
        print("Succès de l'écriture sur le tag RFID.")
        time.sleep(3)  # Attente courte avant de vérifier l'écriture
    except Exception as e:
        print(f"Erreur lors de l'écriture RFID: {e}")
    time.sleep(3)  # Attendre avant de réessayer

# Lecture initiale du tag RFID
read_rfid()

# Écriture sur le tag RFID
write_rfid("TEST RFID")

# Seconde lecture du tag RFID
read_rfid()
