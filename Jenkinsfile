
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-task-manager'
        CONTAINER_NAME = 'flask-task-manager'
        APP_PORT = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading project from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Checking Python application syntax...'
                sh '''
                    python3 -m py_compile app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying Flask application...'
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true

                    docker run -d \
                    --name ${CONTAINER_NAME} \
                    -p ${APP_PORT}:5000 \
                    --restart unless-stopped \
                    ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
