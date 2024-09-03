#!/bin/bash
# Arrêter le processus motion
if ! sudo pkill -f motion; then
  echo "Erreur: Impossible d'arrêter le processus motion."
  exit 1
fi
# Attendre quelques secondes pour s'assurer que le processus est bien arrêté
sleep 5
# Démarrer le processus motion
if ! sudo /usr/bin/motion &; then
  echo "Erreur: Impossible de démarrer le processus motion."
  exit 1
fi
# Attendre quelques secondes pour s'assurer que le processus est bien démarré
sleep 5
echo "Le service motion a été redémarré avec succès. Vous pouvez maintenant vérifier le fonctionnement sur l'interface web."
# Ouvrir l'interface web dans le navigateur par défaut
echo "Pour tester la vidéo, ouvrez le lien suivant dans votre navigateur : http://192.168.253.194:8081/"
