pipeline {
    agent any
    environment {
        AWS_REGION = 'ap-southeast-2'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Cloning GitHub repo to Jenkins') {
            steps {
                script {
                    echo '..... Cloning from the GitHub .....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Chetan713205/Multi-AI-Agent-with-Langgraph.git']])
                }
            }
        }
        
        stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    credentialsId: 'aws-token',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        // Fix Docker socket permissions first
                        sh 'sudo chmod 666 /var/run/docker.sock || true'
                        
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        sh """
                        # Login to ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        
                        # Build the image
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                        
                        # Tag and push
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                        docker push ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker resources
            sh 'docker system prune -f || true'
        }
    }
}