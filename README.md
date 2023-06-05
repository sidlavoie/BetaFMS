# BetaFMS
## Une tentative de créer un système FMS pour la compétition Betabot de Robotique FIRST Québec
### Bases
Le projet s'appuie sur la plateforme développé pour la compétition de Robotique FIRST (FRC). Il utilise le système de contrôle officiel mais adapte le jeu pour une utilisation différente. 
Les détails du système de contrôle officiel sont disponibles [ici](https://docs.wpilib.org/fr/stable/).

### Matériel
Les composantes matériel sont les suivantes:
* Serveur Linux
* Commutateur de couche 3 POE Cisco 3560-24-PS
* Point d'accès Cisco 2602i
* Deux commutateurs de terrain (faisant partie du SCC) Cisco 2960-8-TC-L
* Deux microcontrôleurs WIZnet W6100-EVB-PICO (basé sur le RP2040)

### Logiciel
Le projet s'exécute sur Linux dans un conteneur Docker. Le script de création du conteneur sera rendu publique sous peu. Le logiciel est écrit en Python avec le logiciel des microcontrôleurs 
écrit en C++. Le terrain est divisé en trois VLANs (Vert, Jaune et Admin) ce qui isole la communication entre les robots. Chaque robot est attribué un SSID caché et un mot de passe généré
aléatoirement au début de la compétition. Une base de données SQLite permet de contabiliser le déroulement de l'évènement. Un serveur Web sera créé pour contrôler l'évènement, comme celui utilisé en FTC.

### Avancement
Le projet est en cours de démarrage. PLus de détails seront disponibles sous peu.


## An attempt to make a functionnal FMS for Robotique FIRST Quebec's Betabots
### Bases
This project builds upon the framework developped for the First Robotics Competition (FRC). It uses the official control system, but adapts the game for a different usage.
Details about the oficial control system are available [here](https://docs.wpilib.org/en/stable/).

### Hardware
Hardware components are the following:
* Linux server
* Cisco 3560-24-PS layer 3 POE switch
* Cisco 2602i access point
* Two Cisco 2960-8-TC-L field switches (part of the SCC)
* Two WIZnet W6100-EVB-PICO microcontrollers (based on the RP2040)

### Software
The software runs on Linux in a Docker container. The container script will be made public soon. The software is written in Python, with the microcontroller software being written in C++. 
The field is divided into three VLANs (Vert, Jaune and Admin) which isolates the communication between the robots. Each robot is given an hidden SSID and auto-generated password at the start of
the competition. A SQLite database stores all the informations of the event. A web server will be created in order to control the event, like the one used in the FTC competition.

