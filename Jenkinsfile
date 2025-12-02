pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "catering_backend:latest"
        FRONTEND_IMAGE = "catering_frontend:latest"
        MYSQL_CONTAINER = "catering_mysql"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Ajay6-six/TWO-TIER-Devops-project.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker build -t $BACKEND_IMAGE ./backend'
                    sh 'docker build -t $FRONTEND_IMAGE ./frontend'
                }
            }
        }

        stage('Start Containers') {
            steps {
                script {
                    sh 'docker-compose down'
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'You can add backend API tests or frontend smoke tests here'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Something went wrong!'
        }
    }
}
