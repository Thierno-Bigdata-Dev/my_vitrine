pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_CMD = 'docker compose' // ou 'docker-compose' selon l'installation sur le serveur Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build & Deploy Containers') {
            steps {
                script {
                    echo "Construction et lancement des conteneurs avec Docker Compose..."
                    sh "${DOCKER_COMPOSE_CMD} up -d --build"
                }
            }
        }

        stage('Verify') {
            steps {
                script {
                    echo "Vérification des conteneurs en cours d'exécution..."
                    sh "${DOCKER_COMPOSE_CMD} ps"
                }
            }
        }
    }

    post {
        always {
            echo "Fin du pipeline."
        }
    }
}
