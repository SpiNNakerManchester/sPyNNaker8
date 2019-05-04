pipeline {
    agent {
        docker { image 'python3.6' }
    }
    stages {
        stage('Before Install') {
            environment {
                TRAVIS_BRANCH = "${env.BRANCH_NAME}"
            }
            steps {
                // remove all directories left if Jenkins ended badly
                sh 'rm -rf support SpiNNUtils SpiNNMachine SpiNNStorageHandlers SpiNNMan PACMAN DataSpecification spalloc spinnaker_tools spinn_common SpiNNFrontEndCommon sPyNNaker IntroLab PyNN8Examples JavaSpiNNaker reports'
                sh 'git clone https://github.com/SpiNNakerManchester/SupportScripts.git support'
                sh 'pip3 install --upgrade setuptools wheel'
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
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/PyNN8Examples.git'
                //sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/JavaSpiNNaker'
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
                //sh 'mvn -f JavaSpiNNaker package'
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
                sh 'rm -f .coveragerc'
                sh 'echo "<testsuite tests="0"></testsuite>" > results.xml'
            }
        }
        stage('Test') {
            steps {
                run_pytest('p8_integration_tests/quick_test/', 1200)
            }
        }
        stage('Run scripts') {
            steps {
                sh 'python p8_integration_tests/scripts_test/build_scipt.py'
                run_pytest('py.test p8_integration_tests/scripts_test', 1200)
            }
        }
        //stage('What do they do Tests') {
        //    steps {
        //        sh 'py.test p8_integration_tests/test_csa_connectors --forked --instafail spynnaker8 --timeout 1200'
        //        sh 'py.test p8_integration_tests/test_current_calculation --forked --instafail spynnaker8 --timeout 1200'
        //        sh 'py.test p8_integration_tests/test_if_curr_exp_live_buffers --forked --instafail spynnaker8 --timeout 1200'
        //        sh 'py.test p8_integration_tests/test_live_packet_gather --forked --instafail spynnaker8 --timeout 1200'
        //   }
        //}
        stage('Reports') {
            steps {
                sh 'find reports/* -type f -print -exec cat {}  \\;'
            }
        }
        stage('Check Destroyed') {
            steps {
                sh 'py.test p8_integration_tests/destroyed_checker_test --forked --instafail --timeout 120'
            }
        }
    }
    post {
        success {
            junit 'results.xml'
            cobertura coberturaReportFile: 'coverage.xml'
            cleanWs()
        }
    }
}

def run_pytest(String tests, int timeout) {
    sh 'py.test ${tests} --forked --show-progress --cov spynnaker8 --cov spynnaker --cov spinn_front_end_common --cov pacman --cov data_specification --cov spinnman --cov spinn_machine --cov spinn_storage_handlers --cov spalloc --junitxml results.xml --cov-report xml:coverage.xml --cov-append --timeout ${timeout}'
}
