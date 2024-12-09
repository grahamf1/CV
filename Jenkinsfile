pipeline {
    agent none

    environment {
        COSMOS_DB_CONNECTION_STRING = ''
    }

    stages {
        stage('Get CosmosDB Connection String') {
            agent { label 'Jenkins'}
            steps {
                script {
                    def userInput = input(
                        id: 'userInput', message: 'Please enter the CosmosDB connection string:',
                        parameters: [
                            string(defaultValue: '', description: 'CosmosDB Connection String', name: 'COSMOS_DB_CONNECTION_STRING')
                        ]
                    )
                    env.COSMOS_DB_CONNECTION_STRING = userInput
                }
            }
        }
        stage('Containerise') {
            agent {label 'Jenkins'}
            steps {
                script {
                    echo 'Containerising the Flask app in Docker'
                    sh "docker build --build-arg COSMOS_DB_CONNECTION_STRING='${env.COSMOS_DB_CONNECTION_STRING}' -t my_app ."
                    sh "docker run -d -p 5001:5001 -e COSMOS_DB_CONNECTION_STRING='${env.COSMOS_DB_CONNECTION_STRING}' my_app"
                }
            }
        }
        stage('Test') {
            agent { label 'Jenkins'}
            steps {
                script {
                    echo 'Running tests on Flask application'
                }
            }
        }
    }
}