pipeline {
    agent any

    environment {
        APP_NAME = 'todo-app'
        USERNAME = 'nadaessa'
    }

    stages {
        stage ('Login to DockerHub') {
            withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-todo-token',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    echo ${DOCKERHUB_PASSWORD} | docker login -u ${env.DOCKERHUB_USERNAME} --password-stdin
                }
        }
        stage ('Building Docker Image') {
            steps {
                docker build -t ${env.APP_NAME}:v${env.BUILD_NUMBER} .
            }
        }

        stage ('Pushing the Image to DockerHub') {
            steps {
                docker push ${env.USERNAME}/${env.APP_NAME}
            }
        }

        stage ('Running Docker Container') {
            docker run --name=${env.APP_NAME} -p 5000:5000 ${env.USERNAME}/${env.APP_NAME}:v${env.BUILD_NUMBER}
        }
    }
}