#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file,TEMPLATE_PATH
from joyit_mfrc522 import SimpleMFRC522 
from modules.AlphaBot import AlphaBot
import threading, socket, os, sys, time, subprocess, ssl


TEMPLATE_PATH.append('/home/christian/WebControl/')
car = AlphaBot()
script_process = None
speed = 50  # Valeur de vitesse par défaut

@get("/")
def index():
    return template('templates/index')
@get("/tests")
def tests():
    return template("templates/tests")

# Test programmes
@post('/servo_motor')
def servo_motor():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'tests/servo_motor.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'
@post('/motor_speed_move')
def motor_speed_move():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'tests/motor_speed_move.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'
@post('/infrared_obstacle_module')
def infrared_obstacle_module():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'tests/infrared_obstacle_module.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'
@post('/lidar_module')
def lidar_module():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['sudo', 'python3', 'tests/lidar_module.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'
@post('/rfid_read_write_module')
def rfid_read_write_module():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'tests/rfid_read_write_module.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'

# Fonctionnalité programmes
@post('/infrared_tracking_objects')
def infrared_tracking_objects():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'apps/infrared_tracking_objects.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'
@post('/infrared_obstacle_avoidance')
def infrared_obstacle_avoidance():
    global script_process  # Assurez-vous d'utiliser la variable globale script_process dans cette fonction
    action = request.forms.get('action')
    if action == 'start':
        script_process = subprocess.Popen(['python3', 'apps/infrared_obstacle_avoidance.py'])
    elif action == 'stop' and script_process is not None:
        script_process.terminate()  # Arrêter le script si script_process est défini
    return 'OK'

@post("/cmd")
def cmd():
    global speed  # Déclarer speed comme variable globale pour pouvoir y accéder dans cette fonction
    code = request.body.read().decode()
    speed_str = request.POST.get('speed')
    if speed_str is not None:
        try:
            speed = int(speed_str)
            if 0 <= speed <= 100:
                car.setPWMA(speed)
                car.setPWMB(speed)
                print("Vitesse définie à", speed)
        except ValueError:
            print("") # Invalid speed value

    if code == "stop":
        car.stop()
    elif code == "forward":
        car.forward(speed)
    elif code == "backward":
        car.backward(speed)
    elif code == "turnleft":
        car.left(speed)
    elif code == "turnright":
        car.right(speed)
    else:
        print("") # Unknown command
    return "OK"

@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')
@route('/templates/<filename>')
def server_templates(filename):
    return static_file(filename, root='./templates/')
@route('/images/<filename>')
def server_images(filename):
    return static_file(filename, root='./images/')
@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')
@route('/js/<filename>')
def server_js(filename):
    return static_file(filename, root='./js/')
@route('/css/<filename>')
def server_css(filename):
    return static_file(filename, root='./css/')
@route('/modules/<filename>')
def server_modules(filename):
    return static_file(filename, root='./modules/')
@route('/apps/<filename>')
def server_apps(filename):
    return static_file(filename, root='./apps/')
@route('/tests/<filename>')
def server_tests(filename):
    return static_file(filename, root='./tests/')

# Chemins vers le certificat SSL et la clé privée
certfile = '/home/christian/WebControl/ssl/cert.pem'
keyfile = '/home/christian/WebControl/ssl/key.pem'

# Créez un contexte SSL
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

def wait_for_network():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            localhost = s.getsockname()[0]
            s.close()
            return localhost
        except OSError:
            print("Le réseau est inaccessible. Réessai dans 5 secondes...")
            time.sleep(5)

localhost = wait_for_network()

run(host=localhost, port=8000, server='wsgiref', debug=True, ssl_context=ssl_context)
