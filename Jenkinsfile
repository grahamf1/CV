pipeline {
    agent none

    environment {
        COSMOS_DB_CONNECTION_STRING = credentials('cosmos-db-connection-string')
        CONTAINER_REGISTRY = credentials('container-registry')
        ACR_ADMIN_USERNAME = credentials('acr-admin-username')
        ACR_ADMIN_PASSWORD = credentials('acr-admin-password')
    }

    stages {
        stage('Build') {
            agent {label 'agent-1'}
            steps {
                script {
                    echo 'Building the Flask app in Docker'
                    try {
                        sh """
                            set -x
                            docker build -t cv_app . 
                            docker run -d -p 5000:5000 --name app_container -e AZURE_COSMOS_CONNECTION_STRING="\${COSMOS_DB_CONNECTION_STRING}" cv_app
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
            agent { label 'agent-1'}
            steps {
                script {
                   echo 'Testing Docker container'
                    sh '''
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
                    sh 'docker stop app_container'
                    sh 'docker rm app_container'
                }
            }
        }
         stage('Deploy') {
            agent { label 'agent-1'}
            steps {
                script {
                   echo 'Deploying Docker container'
                    sh '''
                        docker login ${CONTAINER_REGISTRY} --username ${ACR_ADMIN_USERNAME} --password-stdin <<< ${ACR_ADMIN_PASSWORD}
                        echo "$?"
                        docker tag ${CONTAINER_REGISTRY}.azurecr.io/deploy/cv_app
                        docker push ${CONTAINER_REGISTRY}.azurecr.io/deploy/cv_app

                        docker logout ${CONTAINER_REGISTRY}.azurecr.io
                        
                        echo "Container pushed to registry successfully"
                    '''
                }
            }
        }
    }
}