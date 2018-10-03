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
                // C dependencies
                sh 'support/gitclone.sh git://github.com/SpiNNakerManchester/sPyNNaker.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinnaker_tools.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinn_common.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git'
            }
        }
        stage('Install') {
            environment {
                SPINN_DIRS = '${workspace}/spinnaker_tools'
                NEURAL_MODELLING_DIRS = '${workspace}/neural_modelling'
            }
            steps {
                sh 'pip install -r requirements-test.txt'
                sh 'pip install python-coveralls "coverage>=4.4"'
                // C Build
                sh 'make -C $SPINN_DIRS'
                sh 'make -C spinn_common install'
                sh 'make -C SpiNNFrontEndCommon/c_common install'
                sh 'make -C sPyNNaker/neural_modelling'
                // Python install
                sh 'cd sPyNNaker && python setup.py install'
                sh 'python ./setup.py install'
                sh 'python -m spynnaker8.setup_pynn'
            }
        }
        stage('Before Script') {
            steps {
                sh 'echo "[Machine]" > ~/.spynnaker.cfg'
                sh 'echo "spalloc_server = spinnaker.cs.man.ac.uk" >> ~/.spynnaker.cfg'
                sh 'echo "spalloc_user = Jenkins" >> ~/.spynnaker.cfg'
            }
        }
        stage('Script') {
            steps {
                sh 'py.test p8_integration_tests --cov spynnaker8'
            }
        }
        stage('Coverage') {
            steps {
                sh 'COVERALLS_REPO_TOKEN=l0cQjQq6Sm5MGb67RiWkY2WE4r74YFAfk COVERALLS_PARALLEL=true coveralls'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
