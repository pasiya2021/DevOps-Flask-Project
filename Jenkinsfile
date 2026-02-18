pipeline {
    agent any
    
    stages {
        stage('Cleanup') {
            steps {
                sh 'docker system prune -f || true'
            }
        }
        
        stage('Clone Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pasiya2021/DevOps-Flask-Project.git'
            }
        }
        
        stage('Stop Old Containers') {
            steps {
                sh 'docker-compose -f /var/jenkins_home/workspace/Flask-DevOps-Pipeline/docker-compose.yml down || true'
            }
        }
        
        stage('Start New Containers') {
            steps {
                sh 'docker-compose -f /var/jenkins_home/workspace/Flask-DevOps-Pipeline/docker-compose.yml up -d'
            }
        }
    }
    
    post {
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed!'
        }
    }
}
