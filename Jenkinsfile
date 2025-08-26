pipeline{
    agent any
        environment {
            AWS_REGION = 'ap-southeast-2'
            ECR_REPO = 'my-repo'
            IMAGE_TAG = 'latest'
	    }

    	stages {
        	stage('Cloning GitHub repo to Jenkins') {
            		steps{
                		script{
                    			echo '..... Cloning from the GitHub .....'
                    			checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Chetan713205/Multi-AI-Agent-with-Langgraph.git']])
                		}
            		}
        	}

        stages {
            stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-token', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                script {
                    def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                    def ecrUrl    = "${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                    docker push ${ecrUrl}:${IMAGE_TAG}
                    """
                        }
                    }
                }
            }
        }
    }
}
