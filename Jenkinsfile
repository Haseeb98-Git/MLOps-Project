pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'theusername'
        REPOSITORY_NAME = 'mlops-repository-2'
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Set AIRFLOW_UID') {
            steps {
                bat 'echo AIRFLOW_UID=1000 >> .env'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Tag and Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    bat """
                    docker tag mlops-project-mlflow:latest %DOCKERHUB_USERNAME%/%REPOSITORY_NAME%:mlops-proj-mlflow-latest
                    docker tag apache/airflow:3.0.1 %DOCKERHUB_USERNAME%/%REPOSITORY_NAME%:apache-airflow-3.0.1
                    docker tag postgres:13 %DOCKERHUB_USERNAME%/%REPOSITORY_NAME%:postgres-13
                    docker tag redis:7.2-bookworm %DOCKERHUB_USERNAME%/%REPOSITORY_NAME%:redis-7.2-bookworm

                    echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin

                    docker push %DOCKER_USERNAME%/%REPOSITORY_NAME%:mlops-proj-mlflow-latest
                    docker push %DOCKER_USERNAME%/%REPOSITORY_NAME%:apache-airflow-3.0.1
                    docker push %DOCKER_USERNAME%/%REPOSITORY_NAME%:postgres-13
                    docker push %DOCKER_USERNAME%/%REPOSITORY_NAME%:redis-7.2-bookworm
                    """
                }
            }
        }

        stage('Initialize Airflow') {
            steps {
                bat 'docker compose up airflow-init'
            }
        }

        stage('Start Airflow') {
            steps {
                bat 'docker compose up -d'
            }
        }
    }
}
