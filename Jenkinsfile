pipeline {
    agent any

    environment {
        DB_PASSWORD = credentials('db_password') 
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build & Run Containers') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m unittest discover tests'
            }
        }

        stage('Selenium Tests') {
            steps {
                sh 'docker build -f Dockerfile.selenium -t selenium-tests .'
                sh 'docker run --network="host" selenium-tests'
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker-compose down'
            }
        }
    }
}
