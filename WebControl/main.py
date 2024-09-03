#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,redirect,post,run,route,request,response,template,static_file,TEMPLATE_PATH
from joyit_mfrc522 import SimpleMFRC522 
from modules.AlphaBot import AlphaBot
import threading, socket, os, sys, time, subprocess, ssl, json,signal


TEMPLATE_PATH.append('/home/christian/WebControl/')
certfile = '/home/christian/WebControl/ssl/cert.pem'
keyfile = '/home/christian/WebControl/ssl/key.pem'
Ab = AlphaBot()
script_process = None
duration = 1
speed = 30
# Stocke les dernières données reçues
validation_results = {"name": None, "confidence": None}

@get("/")
def index():
        # Chemin vers le fichier JSON
    json_file_path = '/home/christian/WebControl/logs/resultats_tests.json'

    # Lire le fichier JSON
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        last_15_results = data[-10:][::-1]
    return template('templates/index', message="", results=last_15_results)

@get("/tests")
def tests():
    return template("templates/tests")

@get("/access")
def show_validation():
    # Rendre le fichier HTML access.html avec les résultats actuels
    return template("templates/access",name=validation_results["name"],confidence=validation_results["confidence"],status="Aucune validation reçue" if not validation_results["name"] else "Succès")

@post("/access")
def access():
    global validation_results
    # Récupère les données de la requête
    data = request.json
    name = data.get('name')
    confidence = data.get('confidence')
    # Met à jour les résultats
    validation_results["name"] = name
    validation_results["confidence"] = confidence
    # Affiche les résultats dans la console
    print(f"Validation received: Name: {name}, Confidence: {confidence}")
    # Répond avec un succès
    response.status = 200
    return {"status": "success"}

@post("/restartPi")
def restart_pi():
    try:
        # Commande pour redémarrer le Raspberry Pi
        subprocess.run('sudo reboot', shell=True, check=True)
        message = "Redémarrage en cours..."
    except Exception as e:
        # Gestion des erreurs, retour d'un message d'erreur si la commande échoue
        message = f"Erreur lors du redémarrage: {str(e)}"
    # Retourne un message au client
    return template('<b>{{message}}</b><br><form action="/" method="post"><input type="submit" value="Retour"></form>', message=message)

@post("/restartMotion")
def restart_motion():
    try:
        # Arrêter Motion si en cours
        subprocess.run('sudo pkill -f motion', shell=True, check=True)
        # Redémarrer Motion
        subprocess.run('sudo /usr/bin/motion', shell=True, check=True)
        message = 'Motion redémarré'
    except subprocess.CalledProcessError as e:
        # Gestion des erreurs si les commandes échouent
        message = f"Erreur lors du redémarrage de Motion: {str(e)}"
    # Retourner un message au client
    return template('<b>{{message}}</b><br><form action="/" method="post"><input type="submit" value="Retour"></form>', message=message)

@post("/cmd")
def cmd():
    global speed, script_process
    response.content_type = 'application/json'

    # Lecture du code de commande depuis la requête
    code = request.body.read().decode()
    
    # Récupération de la vitesse si elle est présente
    speed_str = request.forms.get('speed')
    if speed_str is not None:
        try:
            speed = int(speed_str)
            if 0 <= speed <= 100:
                Ab.setPWMA(speed)
                Ab.setPWMB(speed)
                print("Vitesse définie à", speed)
            else:
                return json.dumps({"error": "La vitesse doit être comprise entre 0 et 100."})
        except ValueError:
            return json.dumps({"error": "La vitesse doit être un nombre entier."})
    try:
        if code == "stop":
            Ab.stop(duration)
            message = 'Voiture arrêtée'
        elif code == "forward":
            Ab.forward(duration, speed)
            message = 'Voiture en avant'
        elif code == "backward":
            Ab.backward(duration, speed)
            message = 'Voiture en arrière'
        elif code == "turnleft":
            Ab.left(duration, speed)
            message = 'Voiture tourne à gauche'
        elif code == "turnright":
            Ab.right(duration, speed)
            message = 'Voiture tourne à droite'
        # TESTS
        elif code == "testServo":
            script_process = subprocess.Popen(['python3', 'tests/servo_motor.py'])
            message = 'Servo moteur OK'
        elif code == "appRFIDCarDoor":
            script_process = subprocess.Popen(['python3', 'tests/rfid_open_door.py'])
            message = 'Module RFID Door OK'
        elif code == "testRotor":
            script_process = subprocess.Popen(['python3', 'tests/motor_speed_move.py'])
            message = 'Moteurs OK'
        elif code == "testLidar":
            script_process = subprocess.Popen(['sudo', 'python3', 'tests/lidar_module.py'])
            message = 'Module Lidar OK'
        elif code == "testObstacle":
            script_process = subprocess.Popen(['python3', 'tests/infrared_obstacle_module.py'])
            message = 'Module IR obstacle OK'
        #APPS
        elif code == "appRFID":
            script_process = subprocess.Popen(['python3', 'apps/rfid_read_write_module.py'])
            message = 'Lecture et écriture RFID OK'
        elif code == "appLidarSpeed":
            script_process = subprocess.Popen(['sudo', 'python3', 'apps/lidar_speed_move.py'])
            message = 'Régulation de la vitesse par Lidar OK'
        elif code == "appEmergencyStop":
            script_process = subprocess.Popen(['python3', 'apps/infrared_obstacle_avoidance.py'])
            message = 'Emergency STOP par IR OK'
        else:
            return json.dumps({"error": f"Commande inconnue ({code})"})
    except Exception as e:
        return json.dumps({"error": str(e)})
    return json.dumps({"message": message})

@route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./')
@route('/templates/<filename:path>')
def server_templates(filename):
    return static_file(filename, root='./templates/')
@route('/images/<filename:path>')
def server_images(filename):
    return static_file(filename, root='./images/')
@route('/fonts/<filename:path>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')
@route('/js/<filename:path>')
def server_js(filename):
    return static_file(filename, root='./js/')
@route('/css/<filename:path>')
def server_css(filename):
    return static_file(filename, root='./css/')
@route('/modules/<filename:path>')
def server_modules(filename):
    return static_file(filename, root='./modules/')
@route('/apps/<filename:path>')
def server_apps(filename):
    return static_file(filename, root='./apps/')
@route('/tests/<filename:path>')
def server_tests(filename):
    return static_file(filename, root='./tests/')

def wait_for_network():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            localhost = s.getsockname()[0]
            s.close()
            return localhost
        except OSError:
            print("Le réseau est inaccessible. Réessayer dans 5 secondes...")
            time.sleep(5)

localhost = wait_for_network()

# Créez un contexte SSL
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
# run(host=localhost, port=8000, server='wsgiref', debug=True, ssl_context=ssl_context)

run(host=localhost, port=8000, server='wsgiref', debug=True)
