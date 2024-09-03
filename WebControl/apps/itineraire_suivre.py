#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, time, sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()
speed = 20

# Fonction pour calculer la durée en fonction de la distance
def calculate_duration(distance_value):
    # Réglez la vitesse de traitement selon vos besoins
    speed_factor = 0.001  # Exemple 0.01/100m:s | 0.001/1km/s
    return distance_value * speed_factor

# Lecture du fichier selected_steps.json et traitement des manoeuvres
def process_selected_steps(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        selected_steps = json.load(f)

    for step in selected_steps:
        maneuver = step['maneuver']
        distance_value = step['distance_value']
        
        # Calcul de la durée en fonction de la distance
        duration = calculate_duration(distance_value)
        
        if maneuver == "maneuver-unspecified":
            Ab.maneuver_unspecified(duration)
        elif maneuver == "turn-slight-left":
            Ab.turn_slight_left(duration, speed)
        elif maneuver == "turn-sharp-left":
            Ab.turn_sharp_left(duration, speed)
        elif maneuver == "u-turn-left":
            Ab.u_turn_left(duration, speed)
        elif maneuver == "turn-left":
            Ab.left(duration, speed)
        elif maneuver == "turn-slight-right":
            Ab.turn_slight_right(duration, speed)
        elif maneuver == "turn-sharp-right":
            Ab.turn_sharp_right(duration, speed)
        elif maneuver == "u-turn-right":
            Ab.u_turn_right(duration, speed)
        elif maneuver == "turn-right":
            Ab.right(duration, speed)
        elif maneuver == "straight":
            Ab.forward(duration, speed)
        elif maneuver == "ramp-left":
            Ab.ramp_left(duration, speed)
        elif maneuver == "ramp-right":
            Ab.ramp_right(duration, speed)
        elif maneuver == "merge":
            Ab.merge(duration, speed)
        elif maneuver == "fork-left":
            Ab.fork_left(duration, speed)
        elif maneuver == "fork-right":
            Ab.fork_right(duration, speed)
        elif maneuver == "ferry":
            Ab.stop(duration)
        elif maneuver == "ferry-train":
            Ab.stop(duration)
        elif maneuver == "roundabout-left":
            Ab.roundabout_left(duration, speed)
        elif maneuver == "roundabout-right":
            Ab.roundabout_right(duration, speed)
        else:
            print(f"Manoeuvre inconnue : {maneuver}")

# Nom du fichier contenant les étapes sélectionnées
selected_steps_filename = '/home/christian/WebControl/logs/selected_steps_short.json'

# Appel de la fonction pour traiter les étapes sélectionnées
print("Le départ est prévu dans 10 secondes...")
time.sleep(10)
print("Départ imminent !")
process_selected_steps(selected_steps_filename)
