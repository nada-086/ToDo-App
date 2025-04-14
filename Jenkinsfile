pipeline {
    agent any

    stages {
        stage ('Building Docker Image') {
            steps {
                docker build -t todo-app:v${env.BUILD_NUMBER} .
            }
        }

        stage ('Running Docker Container') {
            docker run --name=todo-app -p 5000:5000 nadaessa/todo-app:v${env.BUILD_NUMBER}
        }
    }
}