pipeline {
    agent any

    stages {
        stage('Set AIRFLOW_UID') {
            steps {
                sh 'echo -e "AIRFLOW_UID=$(id -u)" > .env'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Initialize Airflow') {
            steps {
                sh 'docker compose up airflow-init'
            }
        }

        stage('Start Airflow') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
