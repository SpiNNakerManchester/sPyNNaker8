pipeline {
    agent {
        docker { image 'python' }
    }
    stages {
        stage('Before Install') {
            environment {
                TRAVIS_BRANCH = "${env.BRANCH_NAME}"
            }
            steps {
                sh 'rm -rf support'
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
                // C dependencies
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinnaker_tools.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinn_common.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/sPyNNaker.git'
                // scripts
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/IntroLab.git'
            }
        }
        stage('Install') {
            environment {
                SPINN_DIRS = "${workspace}/spinnaker_tools"
                NEURAL_MODELLING_DIRS = "${workspace}/sPyNNaker/neural_modelling"
            }
            steps {
                // C Build
                sh 'make -C $SPINN_DIRS'
                sh 'make -C spinn_common install'
                sh 'make -C SpiNNFrontEndCommon/c_common'
                sh 'make -C SpiNNFrontEndCommon/c_common install'
                sh 'make -C sPyNNaker/neural_modelling'
                // Python install
                sh 'cd SpiNNFrontEndCommon && python setup.py install'
                sh 'cd sPyNNaker && python setup.py install'
                sh 'pip install -r requirements-test.txt'
                sh 'pip install python-coveralls "coverage>=4.4"'
                sh 'pip install pytest-instafail'
                sh 'python ./setup.py install'
                sh 'python -m spynnaker8.setup_pynn'
            }
        }
        stage('Before Script') {
            steps {
                sh 'echo "[Machine]" > ~/.spynnaker.cfg'
                sh 'echo "spalloc_server = 10.11.192.11" >> ~/.spynnaker.cfg'
                sh 'echo "spalloc_user = Jenkins" >> ~/.spynnaker.cfg'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "<testsuite tests="0"></testsuite>" > results.xml'
                //sh 'py.test p8_integration_tests/quick_test --forked --instafail --cov spynnaker8 --junitxml results.xml --timeout 1200'
                sh 'py.test p8_integration_tests/bmp_test --forked --instafail --cov spynnaker8 --junitxml results.xml --timeout 1200'
            }
        }
        //stage('IntroLab') {
        //    steps {
        //        sh 'echo "<testsuite tests="0"></testsuite>" > results.xml'
        //        sh 'py.test p8_integration_tests/introlab_test --forked --instafail --cov spynnaker8 --junitxml results.xml --timeout 1200'
        //    }
        //}
        // Timeout too short or test too long maybe a nightly crome
        //stage('Longer Test') {
        //    steps {
        //        sh 'py.test p8_integration_tests/long_test --forked --instafail --timeout 12000'
        //    }
        //}
        stage('Coverage') {
            steps {
                sh 'COVERALLS_REPO_TOKEN=l0cQjQq6Sm5MGb67RiWkY2WE4r74YFAfk COVERALLS_PARALLEL=true coveralls'
            }
        }
        stage('Reports') {
            steps {
                sh "mkdir -p reports"
                sh 'find reports/* -type f -print -exec cat {}  \\;'
            }
        }
        stage('No Destroyed') {
            steps {
                sh 'py.test p8_integration_tests/destroyed_checker_test --forked --instafail --timeout 120'
            }
        }
    }
    post {
        always {
            junit 'results.xml'
            cleanWs()
        }
    }
}
