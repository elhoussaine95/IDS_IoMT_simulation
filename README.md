# IDS_IoMT_simulation
la mise en œuvre d’une simulation en temps réel du modèle IDS IoMT à l’aide de la plateforme Docker. 
# L’architecture de simulation
L’architecture de simulation repose sur une structure modulaire composée de plusieurs conteneurs Docker distincts :

Conteneurs capteurs : chacun simule un dispositif IoMT, envoyant périodiquement des données vers l’IDS via des sockets réseau.

Conteneur IDS : embarque le modèle de détection entraîné, reçoit les données, les prétraite en temps réel et renvoie une décision (flux normal ou attaque détectée).

Conteneur logger / stockage : responsable de la journalisation des résultats et de la sauvegarde des données pour une analyse ultérieure.

Tous les conteneurs sont connectés via un réseau Docker interne, assurant des communications sécurisées, rapides et isolées. Cette architecture permet de simuler à la fois un flux continu de données provenant de multiples sources et un déploiement réaliste d’un système IDS dans un environnement hospitalier distribué.
# Dev par OUAJBIR EL HOUSSAINE 
