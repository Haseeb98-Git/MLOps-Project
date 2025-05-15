pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'theusername'  // Replace with your Docker Hub username (or leave empty if using credentials)
        REPOSITORY_NAME = 'mlops-repository' // Replace with your Docker Hub repository name
    }

    triggers {
        // Trigger job only on push to the 'production' branch in GitHub
        githubPush()
    }

    stages {
        stage('Set AIRFLOW_UID') {
            steps {
                sh 'echo "AIRFLOW_UID=$(id -u)" > .env'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Tag and Push Docker Images') {
            steps {
                script {
                    // Tag thee images with your Docker Hub username and repository name
                    sh 'docker tag mlops-proj-mlflow:latest $DOCKERHUB_USERNAME/$REPOSITORY_NAME:mlops-proj-mlflow-latest'
                    sh 'docker tag apache/airflow:3.0.1 $DOCKERHUB_USERNAME/$REPOSITORY_NAME:apache-airflow-3.0.1'
                    sh 'docker tag postgres:13 $DOCKERHUB_USERNAME/$REPOSITORY_NAME:postgres-13'
                    sh 'docker tag debian:bookworm-slim $DOCKERHUB_USERNAME/$REPOSITORY_NAME:debian-bookworm-slim'
                    sh 'docker tag redis:7.2-bookworm $DOCKERHUB_USERNAME/$REPOSITORY_NAME:redis-7.2-bookworm'

                    // Login to Docker Hub using Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: 'haseeb-dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Perform Docker login here using the credentials injected by Jenkins
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'

                        // Push the tagged images to Docker Hub
                        sh 'docker push $DOCKER_USERNAME/$REPOSITORY_NAME:mlops-proj-mlflow-latest'
                        sh 'docker push $DOCKER_USERNAME/$REPOSITORY_NAME:apache-airflow-3.0.1'
                        sh 'docker push $DOCKER_USERNAME/$REPOSITORY_NAME:postgres-13'
                        sh 'docker push $DOCKER_USERNAME/$REPOSITORY_NAME:debian-bookworm-slim'
                        sh 'docker push $DOCKER_USERNAME/$REPOSITORY_NAME:redis-7.2-bookworm'
                    }
                }
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
