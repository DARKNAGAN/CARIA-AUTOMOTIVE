import requests

def envoyer_ip_en_db(ip, username, password):
    url = 'http://votre_domaine.com/Voitures.ip'  # Remplacez cela par l'URL de votre endpoint de base de données
    data = {'ip': ip}
    auth = (username, password)
    try:
        response = requests.post(url, data=data, auth=auth)
        if response.status_code == 200:
            print("Adresse IP envoyée avec succès à la base de données.")
        else:
            print("Erreur lors de l'envoi de l'adresse IP à la base de données. Statut :", response.status_code)
    except Exception as e:
        print("Une erreur s'est produite :", str(e))

def obtenir_ip_publique():
    try:
        response = requests.get('http://ifconfig.me/ip')
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("Impossible de récupérer l'adresse IP publique. Statut :", response.status_code)
            return None
    except Exception as e:
        print("Une erreur s'est produite lors de la récupération de l'adresse IP publique :", str(e))
        return None

def main():
    ip = obtenir_ip_publique()
    if ip:
        username = 'user'
        password = 'mdp'
        envoyer_ip_en_db(ip, username, password)

if __name__ == "__main__":
    main()
