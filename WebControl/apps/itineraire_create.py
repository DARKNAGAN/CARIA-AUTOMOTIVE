import requests, json, time

def get_directions(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        directions = response.json()
        return directions
    else:
        return None

def save_steps_to_file(directions, filename):
    if directions and 'routes' in directions and len(directions['routes']) > 0:
        steps = []
        for route in directions['routes']:
            for leg in route['legs']:
                for step in leg['steps']:
                    steps.append(step)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(steps, f, indent=2, ensure_ascii=False)

def save_selected_steps_to_file(directions, filename):
    selected_steps = []
    if directions and 'routes' in directions and len(directions['routes']) > 0:
        for route in directions['routes']:
            for leg in route['legs']:
                for step in leg['steps']:
                    selected_step = {
                        'distance_value': step['distance']['value'],
                        'maneuver': step.get('maneuver', 'maneuver-unspecified')
                    }
                    selected_steps.append(selected_step)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(selected_steps, f, indent=2, ensure_ascii=False)

# Paramètres
origin = "48.8224, 2.2748"  # Coordonnées pour Paris (latitude, longitude)
destination = "48.67912602858551, 2.3860270345466024"  # Coordonnées pour Lyon (latitude, longitude)
api_key = "APIKEY"


# Obtenir les directions
directions = get_directions(origin, destination, api_key)
print("Préparons ensemble votre itinéraire !")
time.sleep(2)
print("Veuillez saisir l'adresse de départ et l'adresse d'arrivée.")
time.sleep(2)
print("Calcul de l'itinéraire en cours : de Paris à Lyon.")
time.sleep(2)

# Sauvegarder les étapes complètes dans un fichier JSON
steps_filename = '/home/christian/WebControl/logs/steps.json'
save_steps_to_file(directions, steps_filename)
# print(f"Les étapes complètes de l'itinéraire ont été sauvegardées dans le fichier {steps_filename}")

# Sauvegarder les étapes sélectionnées dans un fichier JSON
selected_steps_filename = '/home/christian/WebControl/logs/selected_steps.json'
save_selected_steps_to_file(directions, selected_steps_filename)
# print(f"Les étapes sélectionnées de l'itinéraire ont été sauvegardées dans le fichier {selected_steps_filename}")