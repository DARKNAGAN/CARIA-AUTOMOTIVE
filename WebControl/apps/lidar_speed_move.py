import time
import sys
sys.path.append('/home/christian/WebControl/modules/')
from AlphaBot import AlphaBot
Ab = AlphaBot()

# Variable de statut pour indiquer le bon fonctionnement
status = "initialization"

# Durée limite d'exécution en secondes
time_limit = 10
start_time = time.time()
try:
    # Envoi de la commande pour initialiser le capteur
    while True:
        # Vérification si le temps limite est dépassé
        if time.time() - start_time > time_limit:
            break
        
        if Ab.LIDAR_MODULE.in_waiting >= 9:
            if b'Y' == Ab.LIDAR_MODULE.read() and b'Y' == Ab.LIDAR_MODULE.read():
                Dist_L = Ab.LIDAR_MODULE.read()
                Dist_H = Ab.LIDAR_MODULE.read()
                Dist_Total = (Dist_H[0] * 256) + Dist_L[0]
                for i in range(0, 5):
                    Ab.LIDAR_MODULE.read()  # Lecture et ignore des octets supplémentaires
                print("Distance à l'avant du véhicule:", Dist_Total, "cm")
                status = "measurement successful"
                
                # Ajuster la vitesse en fonction de la distance LIDAR
                vitesse_ajustee = Ab.ajuster_vitesse_selon_distance(Dist_Total)
                
                if vitesse_ajustee > 0:
                    Ab.forward(0.1, vitesse_ajustee)  # Avancer avec la vitesse ajustée
                else:
                    Ab.emergencystop()  # S'arrêter si trop proche d'un obstacle
                Ab.LIDAR_MODULE.reset_input_buffer()
except KeyboardInterrupt:
    print("Interruption par l'utilisateur.")
    status = "interrupted"
except Exception as e:
    print(f"Erreur lors de l'exécution: {e}")
    status = "error"
finally:
    Ab.LIDAR_MODULE.close()  # Fermeture propre du port série
    Ab.cleanup()

# Vérification finale et affichage du statut
if status in ["measurement successful"]:
    print("Le composant fonctionne correctement.")
    fonctionnement_ok = True
else:
    print(f"Le composant a rencontré un problème: {status}.")
    fonctionnement_ok = False

Ab.enregistrer_resultats(sys.argv[0], fonctionnement_ok, status)
