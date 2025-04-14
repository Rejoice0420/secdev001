pipeline {
  agent any

  environment {
    IMAGE_NAME = "rejoiceitur/healthcare-app"
    TAG = "latest"
    FULL_IMAGE = "${IMAGE_NAME}:${TAG}"
    CONTAINER_NAME = "healthcare-con1"
    EC2_IP = "54.226.102.176"
    SSH_CREDENTIALS_ID = "ec2-user"
  }

  stages {

    stage('Checkout') {
      steps {
        echo "📦 Cloning source code from GitHub..."
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        echo "🐳 Building Docker image: ${FULL_IMAGE}"
        sh "docker build -t ${FULL_IMAGE} ."
      }
    }

    stage('(Optional) Unit Tests') {
      steps {
        echo "✅ Running unit tests (if any)..."
        // sh './run-tests.sh'
      }
    }

    stage('Push Docker Image') {
      steps {
        echo "🚀 Pushing image to Docker Hub..."
        withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          sh '''#!/bin/bash
            echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
            docker push $FULL_IMAGE
          '''
        }
      }
    }

    stage('Deploy to EC2') {
      steps {
        echo "⚙️ Deploying ${FULL_IMAGE} to EC2 instance ${EC2_IP}..."
        script {
          withCredentials([sshUserPrivateKey(
            credentialsId: SSH_CREDENTIALS_ID,
            keyFileVariable: 'KEY',
            usernameVariable: 'USER'
          )]) {
            sh """#!/bin/bash
              ssh -o StrictHostKeyChecking=no -i "$KEY" "$USER@$EC2_IP" <<EOF
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker pull ${FULL_IMAGE}
                docker run -d --name ${CONTAINER_NAME} -p 8082:8080 ${FULL_IMAGE}
EOF
            """
          }
        }
      }
    }

    stage('Security Scan with Nmap') {
      steps {
        echo "🔒 Running Nmap scan on ${EC2_IP} (port 80)..."
        sh "nmap -A -T4 -p 8080 ${EC2_IP} -oN nmap-scan.txt"
        archiveArtifacts artifacts: 'nmap-scan.txt'
      }
    }
  }

  post {
    success {
      echo "✅ Build, deployment, and scan completed successfully!"
    }
    failure {
      echo "❌ Pipeline failed. Please check the logs."
    }
  }
}
