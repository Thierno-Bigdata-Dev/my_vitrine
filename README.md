# Sénégal Commerce

Bienvenue sur le projet **Sénégal Commerce**. Il s'agit d'une application web développée avec Django, accompagnée d'une base de données PostgreSQL, et configurée pour s'exécuter facilement à l'aide de Docker.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Structure du projet

- `senegal_commerce/` : Contient le code source de l'application Django.
- `Dockerfile` : Instructions pour construire l'image Docker de l'application web.
- `docker-compose.yml` : Configuration des services Docker (web et base de données).

## Installation et exécution

Grâce à Docker Compose, l'installation et le lancement du projet sont grandement simplifiés.

1. **Cloner le dépôt** (si ce n'est pas déjà fait) et se placer dans le répertoire du projet.

2. **Construire et démarrer les conteneurs** :
   ```bash
   docker-compose up -d --build
   ```

   Cette commande va :
   - Construire l'image de l'application web.
   - Démarrer le conteneur de la base de données PostgreSQL (`db`).
   - Appliquer les migrations de la base de données.
   - Démarrer le serveur de développement Django (`web`).

3. **Accéder à l'application** :
   L'application devrait maintenant être accessible à l'adresse suivante : [http://localhost:8002](http://localhost:8002).

## Services Docker

- **Web (`senegal_web_container`)**
  - Image construite à partir du `Dockerfile`.
  - Expose le port `8002` sur l'hôte (mappé sur le `8000` du conteneur).
  - Exécute les migrations et démarre le serveur Django.

- **Base de données (`senegal_db_container`)**
  - Utilise l'image `postgres:15-alpine`.
  - Expose le port `5433` sur l'hôte (mappé sur le `5432` du conteneur).
  - Les données sont persistées dans le volume `postgres_data`.

## Arrêter les conteneurs

Pour arrêter les conteneurs sans détruire les données :
```bash
docker-compose stop
```

Pour arrêter et supprimer les conteneurs, réseaux, et volumes par défaut :
```bash
docker-compose down
```
*(Attention : utilisez `docker-compose down -v` si vous souhaitez également supprimer le volume de la base de données).*
