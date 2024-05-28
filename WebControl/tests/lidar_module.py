import serial
import time

try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)

    # Envoi de la commande pour initialiser le capteur
    ser.write(b'\x42\x57\x02\x00\x00\x00\x01\x06')

    while True:
        if ser.in_waiting >= 9:
            if b'Y' == ser.read() and b'Y' == ser.read():
                Dist_L = ser.read()
                Dist_H = ser.read()
                Dist_Total = (Dist_H[0] * 256) + Dist_L[0]
                for i in range(0, 5):
                    ser.read()  # Lecture et ignore des octets supplémentaires
                print("Distance:", Dist_Total, "cm")
except serial.SerialException as e:
    print("Erreur série:", e)
finally:
    if 'ser' in locals():
        ser.close()  # Fermeture propre du port série
