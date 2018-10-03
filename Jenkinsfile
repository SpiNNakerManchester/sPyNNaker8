pipeline {
    agent {
        docker { image 'python' }
    }
    stages {
        stage('Before Install') {
            steps {
                sh 'git clone https://github.com/SpiNNakerManchester/SupportScripts.git support'
                // Bring pip up to date
                sh 'pip install --upgrade pip setuptools wheel'
                sh 'pip install --only-binary=numpy,scipy,matplotlib numpy scipy matplotlib'
                // SpiNNakerManchester internal dependencies; development mode
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/SpiNNUtils.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/SpiNNMachine.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/SpiNNStorageHandlers.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/SpiNNMan.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/PACMAN.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/DataSpecification.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/spalloc.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git'
                sh 'support/pipinstall.sh git://github.com/SpiNNakerManchester/sPyNNaker.git'
            }
        }
        stage('Install') {
            steps {
                sh 'pip install -r requirements-test.txt'
                sh 'python ./setup.py install'
            }
        }
        stage('Before Script') {
            steps {
                sh 'echo "[Machine]" > ~/.spynnaker.cfg'
                sh 'echo "machineName = $SPINNAKER_BOARD_ADDRESS" >> ~/.spynnaker.cfg'
                sh 'echo "version = ${SPINNAKER_BOARD_VERSION:-5}" >> ~/.spynnaker.cfg'
                sh 'echo "[Database]" >> ~/.spynnaker.cfg'
                sh 'echo "[Simulation]" >> ~/.spynnaker.cfg'
                sh 'echo "[Buffers]" >> ~/.spynnaker.cfg'
            }
        }
    }
    /* post {
        always {
            cleanWs()
        }
    } */
}
