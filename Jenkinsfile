pipeline {
    agent {
        docker { image 'python3.6' }
    }
    options {
        skipDefaultCheckout true
    }
    stages {
        stage('Clean and Checkout') {
            steps {
                sh 'rm -rf ${WORKSPACE}/*'
                sh 'rm -rf ${WORKSPACE}/.[a-zA-Z0-9]*'
            }
        }
        stage('Before Install') {
            environment {
                TRAVIS_BRANCH = "${env.BRANCH_NAME}"
            }
            steps {
                // remove all directories left if Jenkins ended badly
                sh 'git clone https://github.com/SpiNNakerManchester/SupportScripts.git support'
                sh 'pip3 install --upgrade setuptools wheel'
                sh 'pip install --only-binary=numpy,scipy,matplotlib numpy scipy matplotlib'
                // SpiNNakerManchester internal dependencies; development mode
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNUtils.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNMachine.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNStorageHandlers.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNMan.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/PACMAN.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/DataSpecification.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spalloc.git'
                // C dependencies
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinnaker_tools.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinn_common.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/sPyNNaker.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/sPyNNaker8.git'
                // scripts
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/IntroLab.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/PyNN8Examples.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/JavaSpiNNaker'
            }
        }
        stage('Install') {
            environment {
                SPINN_DIRS = "${workspace}/spinnaker_tools"
                NEURAL_MODELLING_DIRS = "${workspace}/sPyNNaker/neural_modelling"
            }
            steps {
                // Install SpiNNUtils first as needed for C build
                sh 'cd SpiNNUtils && python setup.py develop'
                // C Build next as builds files to be installed in Python
                sh 'make -C $SPINN_DIRS'
                sh 'make -C spinn_common install'
                sh 'make -C SpiNNFrontEndCommon/c_common'
                sh 'make -C SpiNNFrontEndCommon/c_common install'
                sh 'make -C sPyNNaker/neural_modelling'
                // Python install
                sh 'cd SpiNNMachine && python setup.py develop'
                sh 'cd SpiNNStorageHandlers && python setup.py develop'
                sh 'cd SpiNNMan && python setup.py develop'
                sh 'cd PACMAN && python setup.py develop'
                sh 'cd DataSpecification && python setup.py develop'
                sh 'cd spalloc && python setup.py develop'
                sh 'cd SpiNNFrontEndCommon && python setup.py develop'
                sh 'cd sPyNNaker && python setup.py develop'
                sh 'cd sPyNNaker8 && python ./setup.py develop'
                sh 'python -m spynnaker8.setup_pynn'
                sh 'pip install -r SpiNNMachine/requirements-test.txt'
                sh 'pip install -r SpiNNStorageHandlers/requirements-test.txt'
                sh 'pip install -r SpiNNMan/requirements-test.txt'
                sh 'pip install -r PACMAN/requirements-test.txt'
                sh 'pip install -r DataSpecification/requirements-test.txt'
                sh 'pip install -r spalloc/requirements-test.txt'
                sh 'pip install -r SpiNNFrontEndCommon/requirements-test.txt'
                sh 'pip install -r sPyNNaker/requirements-test.txt'
                sh 'pip install -r sPyNNaker8/requirements-test.txt'
                sh 'pip install python-coveralls "coverage>=4.4"'
                sh 'pip install pytest-instafail'
                sh 'mvn -f JavaSpiNNaker package'
            }
        }
        stage('Before Script') {
            steps {
                sh 'echo "[Machine]" > ~/.spynnaker.cfg'
                sh 'echo "spalloc_server = 10.11.192.11" >> ~/.spynnaker.cfg'
                sh 'echo "spalloc_user = Jenkins" >> ~/.spynnaker.cfg'
                sh 'echo "enable_advanced_monitor_support = True" >> ~/.spynnaker.cfg'
                sh 'echo "[Java]" >> ~/.spynnaker.cfg'
                sh 'echo "use_java = True" >> ~/.spynnaker.cfg'
                sh 'echo "java_call=/usr/bin/java" >> ~/.spynnaker.cfg'
                sh 'printf "java_spinnaker_path=" >> ~/.spynnaker.cfg'
                sh 'pwd >> ~/.spynnaker.cfg'
                sh 'rm -f coverage.xml'
                sh 'rm -f .coverage'
                sh 'echo "# Empty config" >  ~/.spinnaker.cfg'
                sh 'echo "<testsuite tests="0"></testsuite>" > results.xml'
            }
        }
        stage('Unit Tests') {
            steps {
                run_pytest('SpiNNUtils/unittests', 1200)
                run_pytest('SpiNNStorageHandlers/tests', 1200)
                run_pytest('SpiNNMachine/unittests', 1200)
                run_pytest('SpiNNMan/unittests SpiNNMan/integration_tests', 1200)
                run_pytest('PACMAN/unittests', 1200)
                run_pytest('spalloc/tests', 1200)
                run_pytest('DataSpecification/unittests DataSpecification/integration_tests', 1200)
                run_pytest('SpiNNFrontEndCommon/unittests SpiNNFrontEndCommon/fec_integration_tests', 1200)
                //run_pytest('sPyNNaker/unittests', 1200)
                //run_pytest('sPyNNaker8/unittests', 1200)
            }
        }
        //stage('Test') {
        //    steps {
        //        run_pytest('sPyNNaker8/p8_integration_tests/quick_test/', 1200)
        //    }
        //}
        //stage('Run scripts') {
        //    steps {
        //        sh 'python sPyNNaker8/p8_integration_tests/scripts_test/build_scipt.py'
        //        run_pytest('sPyNNaker8/p8_integration_tests/scripts_test', 1200)
        //    }
        //}
        stage('Reports') {
            steps {
                sh 'find reports/* -type f -print -exec cat {}  \\;'
            }
        }
        stage('Check Destroyed') {
            steps {
                sh 'py.test sPyNNaker8/p8_integration_tests/destroyed_checker_test --forked --instafail --timeout 120'
            }
        }
    }
    post {
        changed {
            script {
                emailext subject: '$DEFAULT_SUBJECT',
                    body: '$DEFAULT_CONTENT',
                    recipientProviders: [
                        [$class: 'CulpritsRecipientProvider'],
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ],
                    replyTo: '$DEFAULT_REPLYTO',
                    to: '$DEFAULT_RECIPIENTS'
            }
        }
        success {
            junit 'results.xml'
            cobertura coberturaReportFile: 'coverage.xml'
            script {
                currentBuild.result = 'SUCCESS'
            }
            step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck', scmVars: [GIT_URL: pullRequest.url]])
        }
    }
}

def run_pytest(String tests, int timeout) {
    sh 'py.test ' + tests + ' -rs --forked --show-progress --cov-branch --cov spynnaker8 --cov spynnaker --cov spinn_front_end_common --cov pacman --cov data_specification --cov spinnman --cov spinn_machine --cov spinn_storage_handlers --cov spalloc --cov spinn_utilities --junitxml results.xml --cov-report xml:coverage.xml --cov-append --timeout ' + timeout
}