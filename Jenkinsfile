pipeline {
    agent {
        label 'jenkins-agent'
    }

    environment {
        IMAGE_NAME = "yeshu008/damageinspection"
        IMAGE_TAG = "${BUILD_ID}"
    }

    // triggers{
    //     pollSCM '*/5 * * * *'
    // }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🔨 Building Docker image..."
                    sh "docker build --no-cache -t $IMAGE_NAME:$IMAGE_TAG ."
                }
            }
        }

        stage('Wait for DB') {
            steps {
                sh 'chmod +x wait-for-db.sh && ./wait-for-db.sh'
            }
        }
        stage('Run Pytest in Docker') {
            steps {
                script {
                    echo "🧪 Running tests inside Docker..."
                    sh '''
                    docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test
                    '''
                }
            }
        }

         stage('Push to Docker Hub') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                echo "📦 Pushing Docker image to Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    sh '''
                    echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        // stage('Deploy (Optional)') {
        //     when {
        //         expression {
        //             return env.BRANCH_NAME == 'main'
        //         }
        //     }
        //     steps {
        //         echo "🚀 Deploying to server or cloud (hook your deploy step here)..."
        //         // Use SCP, SSH, AWS CLI, or Render CLI here
        //     }
        // }
    }

    post {
    always {
        echo "🧹 Cleaning up Docker containers..."
        sh "docker-compose -f docker-compose.test.yml down || true"
    }
    failure {
        echo "❌ Build or test failed."
    }
    success {
        echo "✅ Build, Test, and Push complete."
    }
}

}
