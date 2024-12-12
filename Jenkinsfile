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
                   echo 'Testing Docker container'
                    sh '''
                        sleep 30

                        if ! docker ps | grep -q my_app_container; then
                            echo "Container is not running"
                            exit 1
                        fi

                        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001)
                        if [ $response != "200" ]; then
                            echo "Application is not responding. HTTP status: $response"
                            exit 1
                        fi

                        echo "Container test passed successfully"
                    '''
                }
            }
            post {
                always {
                    sh 'docker stop my_app_container || true'
                    sh 'docker rm my_app_container || true'
                }
            }
        }
    }
}