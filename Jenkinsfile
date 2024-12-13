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
                    writeFile file: 'cosmos_db_connection.txt', text: env.COSMOS_DB_CONNECTION_STRING
                    sh 'echo "COSMOS_DB_CONNECTION_STRING: ${COSMOS_DB_CONNECTION_STRING}"'
                    sh 'cat cosmos_db_connection.txt'
                }
            }
        }
        stage('Containerise') {
            agent {label 'Jenkins'}
            steps {
                script {
                    echo 'Containerising the Flask app in Docker'
                    try {
                        sh """
                            set -x
                            echo "Connection string: ${env.COSMOS_DB_CONNECTION_STRING}"
                            docker build --build-arg COSMOS_DB_CONNECTION_STRING="${env.COSMOS_DB_CONNECTION_STRING}" -t cv_app . 
                            docker run -d -p 5000:5000 --name app_container cv_app
                        """
                    } catch (Exception e) {
                        echo "Docker build failed. Error: ${e.getMessage()}"
                        sh 'cat build.log'
                        error "Docker build failed"
                    }
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

                        echo "Docker container logs:"
                        docker logs app_container

                        if ! docker ps | grep -q app_container 
                        then
                            echo "Container is not running"
                            exit 1
                        fi

                        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)
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
                    sh 'docker stop app_container || true'
                    sh 'docker rm app_container || true'
                }
            }
        }
    }
}