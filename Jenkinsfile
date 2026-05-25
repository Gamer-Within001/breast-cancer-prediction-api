pipeline {
    agent any
    
    environment {
        // These are variables the pipeline will use
        DOCKER_IMAGE = "dakshchauhan001/breast-cancer-api"
        DOCKER_TAG = "latest"
        // In a real Jenkins server, this points to your securely stored password
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "Pulling latest source code from GitHub..."
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building the Docker container..."
                // Windows Jenkins uses 'bat', Linux uses 'sh'
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub..."
                bat "docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%"
                bat "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully! New image is on Docker Hub."
        }
        failure {
            echo "Pipeline failed. Check the logs."
        }
    }
}