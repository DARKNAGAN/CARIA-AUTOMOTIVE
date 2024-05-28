import sys
import os
import subprocess
import signal


def display_menu(scripts):
    print("Choisissez un script à exécuter :")
    for index, script in enumerate(scripts, start=1):
        print(f"{index}. {script}")

def run_python_script(script):
    return subprocess.Popen(["sudo", "python3", script])

def run_python_fct(script):
    # Récupérer le répertoire du script
    script_dir = os.path.dirname(script)
    script_name = os.path.basename(script)
    # Se déplacer vers le répertoire du script et exécuter le script Python
    return subprocess.Popen(["sudo", "python3", script_name], cwd=script_dir)

def run_shell_fct(script):
    # Récupérer le répertoire du script
    script_dir = os.path.dirname(script)
    script_name = os.path.basename(script)
    # Se déplacer vers le répertoire du script et exécuter le script shell
    return subprocess.Popen(["sudo", "./" + script_name], cwd=script_dir)

def main():
    python_scripts = [
        "apps/infrared_tracking_objects.py",
        "apps/infrared_obstacle_avoidance.py",
        "tests/servo_motor.py",
        "tests/motor_speed_move.py",
        "tests/rfid_read_write_module.py",
        "tests/infrared_obstacle_module.py",
        "tests/lidar_module.py"
    ]
    python_fct = [
        "WebControl/main.py"
    ]
    shell_fct = [
    ]

    # Liste pour stocker les PID des processus en cours d'exécution
    running_processes = []

    all_scripts = python_scripts + python_fct + shell_fct

    display_menu(all_scripts)
    choice = input("Votre choix (entrez le numéro du script) : ")

    try:
        choice_index = int(choice) - 1
        if choice_index < 0 or choice_index >= len(all_scripts):
            raise ValueError()
        
        selected_script = all_scripts[choice_index]
        
        # Vérifie si le script est Python ou Shell et l'exécute en conséquence
        if selected_script in python_scripts:
            process = run_python_script(selected_script)
        elif selected_script in python_fct:
            process = run_python_fct(selected_script)
        elif selected_script in shell_fct:
            process = run_shell_fct(selected_script)

        # Ajouter le PID du processus à la liste
        running_processes.append(process.pid)

    except (ValueError, IndexError):
        print("Choix invalide.")
        sys.exit(1)

    # Afficher les PID des processus en cours d'exécution
    print("PID des processus en cours d'exécution :")
    for pid in running_processes:
        print(pid)

    # Attente de l'arrêt du programme
    input("Appuyez sur Entrée pour quitter...")

    # Boucle pour terminer tous les processus en cours d'exécution
    print("Termination des processus en cours...")
    for pid in running_processes:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Processus {pid} terminé.")
        except ProcessLookupError:
            print(f"Le processus {pid} n'existe plus.")

if __name__ == "__main__":
    main()
