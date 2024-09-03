import time,json, os, serial, threading, queue
import RPi.GPIO as GPIO
from datetime import datetime

class AlphaBot(object):    
	def __init__(self):
		self.LIDAR_MODULE = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)  # SERIAL
		self.LIDAR_MODULE.write(b'\x42\x57\x02\x00\x00\x00\x01\x06')
		self.RED_LIGHT = 17
		self.OBSTACLE_PIN = 16
		self.SERVO_PIN = 22
		self.IN1 = 12
		self.IN2 = 13
		self.ENA = 6
		self.IN3 = 20
		self.IN4 = 21
		self.ENB = 26
		speed = 30
		self.stop_event_obstacle = threading.Event()
		self.stop_event_vitesse = threading.Event()
		self.vitesse_queue = queue.Queue()

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.OBSTACLE_PIN, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.SERVO_PIN, GPIO.OUT)
		GPIO.setup(self.RED_LIGHT, GPIO.OUT)
		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		GPIO.setup(self.IN3, GPIO.OUT)
		GPIO.setup(self.IN4, GPIO.OUT)
		GPIO.setup(self.ENA, GPIO.OUT)
		GPIO.setup(self.ENB, GPIO.OUT)
		self.PWMA = GPIO.PWM(self.ENA, 500)  # Utilisation d'une fréquence de 500 Hz pour le PWM
		self.PWMB = GPIO.PWM(self.ENB, 500)
		self.PWMSERVO = GPIO.PWM(self.SERVO_PIN, 50)  # Utilisation d'une fréquence de 50 Hz pour le servo
		self.PWMA.start(0)  # Démarre avec un rapport cyclique de 0 (moteurs arrêtés)
		self.PWMB.start(0)
		self.PWMSERVO.start(0)
		time.sleep(1)
		GPIO.output(self.RED_LIGHT, GPIO.HIGH)


	def ajuster_vitesse_selon_distance(self, distance, vitesse_max=70, vitesse_min=20):
		if distance < 20:  # Distance critique, arrêt
			vitesse = 0
		elif distance < 50:  # Très proche, ralentir
			vitesse = vitesse_min
		else:  # Vitesse normale
			vitesse = vitesse_max * (distance / 100)
			vitesse = max(vitesse_min, min(vitesse, vitesse_max))
		return vitesse

	#Set function to calculate percent from angle servo mettre time sleep après la déclaration
	def set_angle(self, angle) :
		if angle > 120 or angle < 0 :
			return False
		start = 4
		end = 12.5
		ratio = (end - start)/120 #Calcul ratio from angle to percent
		angle_as_percent = angle * ratio
		return start + angle_as_percent

	def blink_led(self, blink_duration=0.2):
		self.blinking = True
		while self.blinking:  # Continue tant que blinking est True
			GPIO.output(self.RED_LIGHT, GPIO.HIGH)
			time.sleep(blink_duration)
			GPIO.output(self.RED_LIGHT, GPIO.LOW)
			time.sleep(blink_duration)
		GPIO.output(self.RED_LIGHT, GPIO.LOW)

	# Fonction pour les manœuvres non spécifiées
	def maneuver_unspecified(self, duration):
		GPIO.output(self.RED_LIGHT, GPIO.HIGH)
		print("Manoeuvre non spécifiée")
		time.sleep(duration)

	def stop(self, duration):
		GPIO.output(self.RED_LIGHT, GPIO.HIGH)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		print(f"Arrêt durant {duration} secondes")
		time.sleep(duration)
		GPIO.output(self.RED_LIGHT, GPIO.LOW)

	def emergencystop(self):
		# Lancer le clignotement dans un thread séparé
		blink_thread = threading.Thread(target=self.blink_led)
		blink_thread.start()
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		print("Arrêt d'urgence !")
		time.sleep(0.1)
        # Stopper le clignotement de la LED
		self.blinking = False
		blink_thread.join()  # Attendre que le thread de clignotement se termine


# FORWARD MOVE		
	def forward(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Avancer durant {duration} secondes à une vitesse de", speed)
		time.sleep(duration)

	def ramp_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 1.5)
		print(f"Traitement pour prendre la rampe de gauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)
		
	def fork_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 1.1)
		print(f"Traitement pour prendre la fourche de gauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)
	
	def ramp_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed * 1.5)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Traitement pour prendre la rampe de droite durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def fork_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 1.1)
		print(f"Traitement pour prendre la fourche de droite durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)
	
	def merge(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed * 0.8)
		self.PWMB.ChangeDutyCycle(speed  * 0.8)
		print(f"Traitement pour fusionner dans le trafic durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)
# BACKWARD MOVE
	def backward(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Reculer durant {duration} secondes à une vitesse de", speed)
		time.sleep(duration)

# LEFT MOVE
	def left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Tourner à guauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)
	
	def turn_slight_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 0.1)
		print(f"Traitement pour tourner légèrement à gauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def turn_sharp_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 1)
		print(f"Traitement pour tourner brusquement à gauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def u_turn_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Traitement pour faire demi-tour à gauche durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration * 2)

	def roundabout_left(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 0.5)
		print(f"Traitement pour tourner à gauche au rond-point durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

# RIGHT MOVE
	def right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Tourner à droite durant {duration} secondes à une vitesse de", speed)
		time.sleep(duration)

	def turn_slight_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed * 0.1)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Traitement pour tourner légèrement à droite durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def turn_sharp_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed * 1)
		print(f"Traitement pour tourner brusquement à droite durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def u_turn_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Traitement pour faire demi-tour à droite durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration * 2)

	def roundabout_right(self, duration, speed):
		GPIO.output(self.RED_LIGHT, GPIO.LOW)
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed * 0.5)
		self.PWMB.ChangeDutyCycle(speed)
		print(f"Traitement pour tourner à droite au rond-point durant {duration} secondes à une vitesse de", speed,"MPH")
		time.sleep(duration)

	def setPWMA(self, value):
		"""
		Ajuste la vitesse du moteur A (gauche).
		:param value: La valeur du rapport cyclique en pourcentage (0-100).
		"""
		self.PWMA.ChangeDutyCycle(value)

	def setPWMB(self, value):
		"""
		Ajuste la vitesse du moteur B (droite).
		:param value: La valeur du rapport cyclique en pourcentage (0-100).
		"""
		self.PWMB.ChangeDutyCycle(value)

	def setMotor(self, left, right):
		"""
		Contrôle individuellement les vitesses des moteurs gauche et droit.
		:param left: La vitesse du moteur gauche en pourcentage (0-100).
		:param right: La vitesse du moteur droit en pourcentage (0-100).
		"""
		self.PWMA.ChangeDutyCycle(left)
		self.PWMB.ChangeDutyCycle(right)

# Fonction pour surveiller les obstacle en arrière-plan
	def monitor_obstacle(self):
		global emergency_stop
		while not self.stop_event_obstacle.is_set():
			DR_status = GPIO.input(self.OBSTACLE_PIN)
			if DR_status == 0:  # Obstacle détecté
				self.emergencystop()
				emergency_stop = True
				while GPIO.input(self.OBSTACLE_PIN) == 0:  # Attendre que l'obstacle soit dégagé
					time.sleep(0.1)
				print("Obstacle dégagé. Attente de 5 secondes avant de reprendre.")
				emergency_stop = False
			time.sleep(0.05)  # Pause légère pour éviter la surcharge du CPU

	def monitor_vitesse(self):
		try:
			while not self.stop_event_vitesse.is_set():
				if self.LIDAR_MODULE.in_waiting >= 9:
					if b'Y' == self.LIDAR_MODULE.read() and b'Y' == self.LIDAR_MODULE.read():
						Dist_L = self.LIDAR_MODULE.read()
						Dist_H = self.LIDAR_MODULE.read()
						Dist_Total = (Dist_H[0] * 256) + Dist_L[0]
						for i in range(0, 5):
							self.LIDAR_MODULE.read()  # Lecture et ignore des octets supplémentaires
						print("Distance à l'avant du véhicule:", Dist_Total, "cm")
						# Définir les paramètres de vitesse
						vitesse_max = 50  # Vitesse maximale en unités (à ajuster)
						distance_min = 10  # Distance minimale pour une vitesse de 0 (en cm)
						# Ajuster la vitesse en fonction de la distance mesurée
						if Dist_Total <= distance_min:
							vitesse_ajustee = 0  # Arrêter si trop proche
						elif Dist_Total > 100:  # Distance maximale où la vitesse est maximale
							vitesse_ajustee = vitesse_max
						else:
							# Calculer la vitesse en fonction de la distance
							vitesse_ajustee = int(vitesse_max * (Dist_Total - distance_min) / (100 - distance_min))
						# Mettre la vitesse ajustée dans la queue
						self.vitesse_queue.put(vitesse_ajustee)
		except Exception as e:
			print(f"Erreur lors de la mesure de la vitesse: {e}")
			# En cas d'erreur, vous pouvez décider de placer une valeur par défaut dans la queue
			self.vitesse_queue.put(None)

	def cleanup(self):
		GPIO.cleanup()
		print("Nettoyage des GPIO effectué.")

	def enregistrer_resultats(self, nom_script, fonctionnement_ok, status):
			# Préparer les données à enregistrer
			nouveau_resultat = {
				'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				'nom': nom_script,
				'fonctionnement_ok': fonctionnement_ok,
				'status': status
			}
			# Chemin vers le fichier de logs
			fichier_logs = './logs/resultats_tests.json'
			# Charger les données existantes si le fichier existe
			if os.path.exists(fichier_logs):
				with open(fichier_logs, 'r') as f:
					try:
						resultats = json.load(f)
					except json.JSONDecodeError:
						resultats = []
			else:
				resultats = []
			# Ajouter le nouveau résultat
			resultats.append(nouveau_resultat)
			# Enregistrer les résultats mis à jour dans le fichier JSON
			with open(fichier_logs, 'w') as f:
				json.dump(resultats, f, indent=4)
			print("Résultats enregistrés avec succès.")