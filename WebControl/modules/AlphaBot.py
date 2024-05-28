import RPi.GPIO as GPIO
import time
import os

class AlphaBot(object):    
	def __init__(self, in1=12, in2=13, ena=6, in3=20, in4=21, enb=26):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb
		# Définition des broches module d'évitement d'obstacles
		DAOUT_PIN = 19
		AOUT_PIN = 16

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IN1, GPIO.OUT)
		GPIO.setup(self.IN2, GPIO.OUT)
		GPIO.setup(self.IN3, GPIO.OUT)
		GPIO.setup(self.IN4, GPIO.OUT)
		GPIO.setup(self.ENA, GPIO.OUT)
		GPIO.setup(self.ENB, GPIO.OUT)
		self.PWMA = GPIO.PWM(self.ENA, 500)  # Utilisation d'une fréquence de 500 Hz pour le PWM
		self.PWMB = GPIO.PWM(self.ENB, 500)
		self.PWMA.start(0)  # Démarre avec un rapport cyclique de 0 (moteurs arrêtés)
		self.PWMB.start(0)

	def stop(self):
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		print("Le robot est arreté")
			
	def forward(self, speed):
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)

		print("Le robot avance avec une vitesse de", speed)

	def backward(self, speed):
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.HIGH)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		self.PWMA.ChangeDutyCycle(speed)
		self.PWMB.ChangeDutyCycle(speed)
		print("Le robot recul avec une vitesse de", speed)

	def left(self, speed):
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMA.ChangeDutyCycle(speed)
		print("Le robot tourne à guauche avec une vitesse de", speed)

	def right(self, speed):
		GPIO.output(self.IN1, GPIO.LOW)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.HIGH)
		GPIO.output(self.IN4, GPIO.LOW)
		self.PWMB.ChangeDutyCycle(speed)
		print("Le robot tourne à droite avec une vitesse de", speed)

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

	def objetrack_ir(self):
		os.system('sudo python3 ~/AppControl/Infrared_Tracking_Objects.py')

	def linetrack_ir(self):
		os.system('sudo python3 ~/AppControl/Infrared_Line_Tracking.py')

	def objetavoid_ir(self):
		os.system('sudo python3 ~/AppControl/Infrared_Obstacle_Avoidance.py')

	def obstacleavoid_ultrason(self):
		os.system('sudo python3 ~/AppControl/Ultrasonic_Obstacle_Avoidance.py')

	def move_ultrason(self):
		os.system('sudo python3 ~/AppControl/Ultrasonic_Ranging.py')

	def control_ir(self):
		os.system('sudo python3 ~/AppControl/Infrared_Remote_Control.py')

	def face_ia(self):
		os.system('sudo python3 ~/AppControl/visage_camera_raspberry.py')

	def line_ia(self):
		os.system('sudo python3 ~/AppControl/visage_camera_v2_raspberry.py')