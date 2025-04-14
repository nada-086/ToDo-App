pipeline {
    agent any

    environment {
        APP_NAME = 'todo-app'
        USERNAME = 'nadaessa'
        DOCKERHUB_TOKEN = 'dockerhub-todo-token'
    }

    stages {
        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-todo-token',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                    '''
                }
            }
        }

        stage('Building Docker Image') {
            steps {
                sh '''
                    docker build -t ${APP_NAME}:v${BUILD_NUMBER} .
                '''
            }
        }

        stage('Pushing the Image to DockerHub') {
            steps {
                sh '''
                    docker tag ${APP_NAME}:v${BUILD_NUMBER} ${USERNAME}/${APP_NAME}:v${BUILD_NUMBER}
                    docker push ${USERNAME}/${APP_NAME}:v${BUILD_NUMBER}
                '''
            }
        }

        stage('Running Docker Container') {
            steps {
                sh '''
                    docker run --name=${APP_NAME} -p 5000:5000 -d ${USERNAME}/${APP_NAME}:v${BUILD_NUMBER}
                '''
            }
        }
    }
}