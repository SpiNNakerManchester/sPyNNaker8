pipeline {
    agent {
        docker { image 'python' }
    }
    stages {
        stage('Before Install') {
            steps {
                sh 'git clone https://github.com/SpiNNakerManchester/SupportScripts.git support'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
