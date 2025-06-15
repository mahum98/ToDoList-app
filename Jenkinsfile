pipeline {
    agent any

    environment {
        DB_PASSWORD = credentials('db_password') 
    }

    stages {
        stage('Code Linting') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 app.py'
            }
        }

        stage('Clone Repository') {
            steps {
                git 'https://github.com/mahum98/ToDoList-app.git'
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
                sh 'docker run --rm --network=host selenium-tests'
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker-compose down'
            }
        }
    }
}
