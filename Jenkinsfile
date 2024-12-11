pipeline {
    agent { label 'Build' }  // Replace 'your-agent-label' with the actual label of your agent
    stages {
        stage('Containerise') {
            steps {
                script {
                    echo 'Containerising the Flask app in Docker'

                    sh 'docker build -t my_app .'

                    sh 'docker run -d -p 5001:5001 my_app'
                }
            }
        }
    }
}