#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot

# Test de la classe AlphaBot avec différentes vitesses pour les moteurs individuels
def test_alphabot_speed():
    bot = AlphaBot()
    try:
        while True:  # Boucle infinie
            for speed in range(20, 101, 40):
                print(f"Test de vitesse à {speed}%")
                
                # Vérifier si speed est une chaîne non vide
                if speed != '':
                    # Test des moteurs en avance
                    bot.forward(speed)
                    time.sleep(1)
                    bot.stop()
                    time.sleep(0.5)
                    
                    # Test des moteurs en arrière
                    bot.backward(speed)
                    time.sleep(1)
                    bot.stop()
                    time.sleep(0.5)
                    
                    # Test du moteur gauche en avant et moteur droit en arrière
                    bot.left(speed)
                    time.sleep(1)
                    bot.stop()
                    time.sleep(0.5)
                    
                    # Test du moteur gauche en arrière et moteur droit en avant
                    bot.right(speed)
                    time.sleep(1)
                    bot.stop()
                    time.sleep(0.5)
    except KeyboardInterrupt:
        bot.cleanup()

if __name__ == "__main__":
    test_alphabot_speed()
