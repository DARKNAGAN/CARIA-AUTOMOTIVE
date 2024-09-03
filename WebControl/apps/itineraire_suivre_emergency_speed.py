#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import json, time, sys
from threading import Thread

sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

status = "initialization"

base_speed = 20  # Vitesse fixe de 20
current_step_index = 0
emergency_stop = False
remaining_duration = 0
adjusted_speed = Ab.vitesse_queue.get()

# Fonction pour calculer la durée en fonction de la distance
def calculate_duration(distance_value):
    speed_factor = 0.001  # Exemple 0.01/100m:s | 0.001/1km/s
    return distance_value * speed_factor

def execute_maneuver(maneuver_function, duration):
    global remaining_duration
    start_time = time.time()
    while not emergency_stop and (time.time() - start_time) < duration:
        time_slice = min(remaining_duration, duration - (time.time() - start_time))
        
        # Lire la vitesse ajustée de la queue si disponible
        if not Ab.vitesse_queue.empty():
            adjusted_speed = Ab.vitesse_queue.get()
        else:
            adjusted_speed = base_speed  # Utiliser la vitesse de base si la queue est vide

        # Appel de la fonction manoeuvre avec la vitesse ajustée
        maneuver_function(time_slice, adjusted_speed)
        
        remaining_duration = duration - (time.time() - start_time)


# Fonction pour traiter les étapes sélectionnées
def process_selected_steps(filename):
    global current_step_index, remaining_duration

    with open(filename, 'r', encoding='utf-8') as f:
        selected_steps = json.load(f)

    while current_step_index < len(selected_steps):
        if emergency_stop:  # Si arrêt d'urgence, attendre que l'obstacle soit dégagé
            time.sleep(0.1)
            continue

        step = selected_steps[current_step_index]
        maneuver = step['maneuver']
        distance_value = step['distance_value']
        duration = calculate_duration(distance_value)
        remaining_duration = duration  # Initialiser la durée restante

        # Appel de la fonction de manoeuvre avec une vitesse fixe de 20
        if maneuver == "maneuver-unspecified":
            execute_maneuver(Ab.maneuver_unspecified, adjusted_speed)
        elif maneuver == "turn-slight-left":
            execute_maneuver(Ab.turn_slight_left, duration, adjusted_speed)
        elif maneuver == "turn-sharp-left":
            execute_maneuver(Ab.turn_sharp_left, duration, adjusted_speed)
        elif maneuver == "u-turn-left":
            execute_maneuver(Ab.u_turn_left, duration, adjusted_speed)
        elif maneuver == "turn-left":
            execute_maneuver(Ab.left, duration, adjusted_speed)
        elif maneuver == "turn-slight-right":
            execute_maneuver(Ab.turn_slight_right, duration, adjusted_speed)
        elif maneuver == "turn-sharp-right":
            execute_maneuver(Ab.turn_sharp_right, duration, adjusted_speed)
        elif maneuver == "u-turn-right":
            execute_maneuver(Ab.u_turn_right, duration, adjusted_speed)
        elif maneuver == "turn-right":
            execute_maneuver(Ab.right, duration, adjusted_speed)
        elif maneuver == "straight":
            execute_maneuver(Ab.forward, duration, adjusted_speed)
        elif maneuver == "ramp-left":
            execute_maneuver(Ab.ramp_left, duration, adjusted_speed)
        elif maneuver == "ramp-right":
            execute_maneuver(Ab.ramp_right, duration, adjusted_speed)
        elif maneuver == "merge":
            execute_maneuver(Ab.merge, duration, adjusted_speed)
        elif maneuver == "fork-left":
            execute_maneuver(Ab.fork_left, duration, adjusted_speed)
        elif maneuver == "fork-right":
            execute_maneuver(Ab.fork_right, duration, adjusted_speed)
        elif maneuver == "ferry":
            execute_maneuver(Ab.stop, duration)
        elif maneuver == "ferry-train":
            execute_maneuver(Ab.stop, duration)
        elif maneuver == "roundabout-left":
            execute_maneuver(Ab.roundabout_left, duration, adjusted_speed)
        elif maneuver == "roundabout-right":
            execute_maneuver(Ab.roundabout_right, duration, adjusted_speed)
        else:
            print(f"Manoeuvre inconnue : {maneuver}")

        # Incrémenter l'index de l'étape seulement si l'arrêt d'urgence n'a pas été déclenché
        if not emergency_stop:
            current_step_index += 1

# Nom du fichier contenant les étapes sélectionnées
selected_steps_filename = '/home/christian/WebControl/logs/selected_steps_short.json'

# Démarrer la surveillance des obstacle dans un thread séparé
vitesse_thread = Thread(target=Ab.monitor_vitesse)
vitesse_thread.daemon = True
vitesse_thread.start()
print("Surveillance de la vitesse en cours")

# Démarrer la surveillance des obstacle dans un thread séparé
obstacle_thread = Thread(target=Ab.monitor_obstacle)
obstacle_thread.daemon = True
obstacle_thread.start()
print("Surveillance d'obstacle en cours")

# Attendre avant de démarrer
print("Le départ est prévu dans 10 secondes...")
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.HIGH)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.HIGH)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
print("5 secondes...")
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.HIGH)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.HIGH)
time.sleep(1)
GPIO.output(Ab.RED_LIGHT, GPIO.LOW)
time.sleep(1)
print("Départ imminent !")
try:
    # Appel de la fonction pour traiter les étapes sélectionnées
    # Appel de la fonction pour traiter les étapes sélectionnées
    process_selected_steps(selected_steps_filename)
    status = "scenario successful"
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
except Exception as e:
    print(f"Erreur lors de l'exécution: {e}")
    status = "error"
finally:
    # Arrêter les threads
    Ab.stop_event_vitesse.set()
    Ab.stop_event_obstacle.set()
    # Attendre que les threads se terminent
    vitesse_thread.join()
    obstacle_thread.join()
    print("Fin de surveillance de la vitesse")
    print("Fin de la surveillance d'obstacle")

    Ab.LIDAR_MODULE.close()  # Fermeture propre du port série
    Ab.cleanup()

# Vérification finale et affichage du statut
if status in ["scenario successful"]:
    print("Le scenario fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le scenario a rencontré un problème : {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)