/*
# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
pipeline {
    agent {
        docker { image 'python3.6' }
    }
    environment {
        // This is where 'pip install --user' puts things
        PATH = "$HOME/.local/bin:$PATH"
        BINARY_LOGS_DIR = "${workspace}"
    }
    options {
        skipDefaultCheckout true
    }
    stages {
        stage('Clean and Checkout') {
            steps {
                sh 'rm -rf ${WORKSPACE}/*'
                sh 'rm -rf ${WORKSPACE}/.[a-zA-Z0-9]*'
                dir('sPyNNaker8') {
                    checkout scm
                }
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
                sh 'pip install --user --upgrade pip'
                // SpiNNakerManchester internal dependencies; development mode
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNUtils.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNMachine.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNMan.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/PACMAN.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/DataSpecification.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spalloc.git'
                // C dependencies
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinnaker_tools.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/spinn_common.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/sPyNNaker.git'
                // Java dependencies
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/JavaSpiNNaker'
                // scripts
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/IntroLab.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/PyNN8Examples.git'
                sh 'support/gitclone.sh https://github.com/SpiNNakerManchester/sPyNNaker8NewModelTemplate.git'
                sh 'support/gitclone.sh git@github.com:SpiNNakerManchester/microcircuit_model.git'
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
                sh 'make -C sPyNNaker8NewModelTemplate/c_models'
                // Python install
                sh 'cd SpiNNMachine && python setup.py develop'
                sh 'cd SpiNNMan && python setup.py develop'
                sh 'cd PACMAN && python setup.py develop'
                sh 'cd DataSpecification && python setup.py develop'
                sh 'cd spalloc && python setup.py develop'
                sh 'cd SpiNNFrontEndCommon && python setup.py develop'
                sh 'cd sPyNNaker && python setup.py develop'
                sh 'cd sPyNNaker8 && python ./setup.py develop'
                sh 'cd sPyNNaker8NewModelTemplate && python ./setup.py develop'
                sh 'python -m spynnaker8.setup_pynn'
                // Test requirements
                sh 'pip install -r SpiNNMachine/requirements-test.txt'
                sh 'pip install -r SpiNNMan/requirements-test.txt'
                sh 'pip install -r PACMAN/requirements-test.txt'
                sh 'pip install -r DataSpecification/requirements-test.txt'
                sh 'pip install -r spalloc/requirements-test.txt'
                sh 'pip install -r SpiNNFrontEndCommon/requirements-test.txt'
                sh 'pip install -r sPyNNaker/requirements-test.txt'
                sh 'pip install -r sPyNNaker8/requirements-test.txt'
                // Additional requirements for testing here
                // coverage version capped due to https://github.com/nedbat/coveragepy/issues/883
                sh 'pip install python-coveralls "coverage>=5.0.0"'
                sh 'pip install pytest-instafail "pytest-xdist==1.34.0"'
                // Java install
                sh 'mvn -f JavaSpiNNaker package'
            }
        }
        stage('Before Script') {
            steps {
                // Write a config file for spalloc and java use
                sh 'echo "[Machine]" > ~/.spynnaker.cfg'
                sh 'echo "spalloc_server = 10.11.192.11" >> ~/.spynnaker.cfg'
                sh 'echo "spalloc_user = Jenkins" >> ~/.spynnaker.cfg'
                sh 'echo "enable_advanced_monitor_support = True" >> ~/.spynnaker.cfg'
                sh 'echo "[Java]" >> ~/.spynnaker.cfg'
                sh 'echo "use_java = True" >> ~/.spynnaker.cfg'
                sh 'echo "java_call=/usr/bin/java" >> ~/.spynnaker.cfg'
                sh 'echo "java_properties=-Dspinnaker.parallel_tasks=10" >> ~/.spynnaker.cfg'
                sh 'printf "java_spinnaker_path=" >> ~/.spynnaker.cfg'
                sh 'pwd >> ~/.spynnaker.cfg'
                // Prepare coverage
                sh 'rm -f coverage.xml'
                sh 'rm -f .coverage'
                sh 'echo "[run]" > .coveragerc'
                sh 'echo "parallel = True" >> .coveragerc'
                // Prepare for unit tests
                sh 'echo "# Empty config" >  ~/.spinnaker.cfg'
                // Create a directory for test outputs
                sh 'mkdir junit/'
            }
        }
        stage('Unit Tests') {
            steps {
                run_pytest('SpiNNUtils/unittests', 1200, 'SpiNNUtils', 'auto')
                run_pytest('SpiNNMachine/unittests', 1200, 'SpiNNMachine', 'auto')
                run_pytest('SpiNNMan/unittests', 1200, 'SpiNNMan', 'auto')
                run_pytest('PACMAN/unittests', 1200, 'PACMAN', 'auto')
                run_pytest('spalloc/tests', 1200, 'spalloc', '1')
                run_pytest('DataSpecification/unittests', 1200, 'DataSpecification', 'auto')
                run_pytest('SpiNNFrontEndCommon/unittests SpiNNFrontEndCommon/fec_integration_tests', 1200, 'SpiNNFrontEndCommon', 'auto')
                run_pytest('sPyNNaker/unittests', 1200, 'sPyNNaker', 'auto')
                run_pytest('sPyNNaker8/unittests', 1200, 'sPyNNaker8', 'auto')
                sh "python -m spinn_utilities.executable_finder"
            }
        }
        stage('Test') {
            steps {
                run_pytest('sPyNNaker8/p8_integration_tests/quick_test/', 1200, 'sPyNNaker8_Integration', 'auto')
            }
        }
        stage('Run new Model Example') {
            steps {
                run_pytest('sPyNNaker8/p8_integration_tests/test_new_model_templates', 1200, 'new_model_example', 'auto')
                run_pytest('sPyNNaker8NewModelTemplate/nmt_integration_tests', 1200, 'nmt_integration_tests', 'auto')
            }
        }
        stage('Run example scripts') {
            steps {
                sh 'python sPyNNaker8/p8_integration_tests/scripts_test/build_script.py shorter'
                run_pytest('sPyNNaker8/p8_integration_tests/scripts_test/examples_auto_test.py', 1200, 'sPyNNaker8Scripts', 'auto')
                run_pytest('sPyNNaker8/p8_integration_tests/scripts_test/intro_labs_auto_test.py', 1200, 'sPyNNaker8Scripts', '1')
                // Not sPyNNaker8/p8_integration_tests/scripts_test/test_microcircuit.py as it takes 1558  seconds
            }
        }
        stage('Reports') {
            steps {
                sh 'find . -maxdepth 3 -type f -wholename "*/reports/*" -print -exec cat \\{\\}  \\;'
                sh "python -m spinn_utilities.executable_finder"
            }
        }
        stage('Check Destroyed') {
            steps {
                sh 'py.test sPyNNaker8/p8_integration_tests/destroyed_checker_test --forked --instafail --timeout 120'
            }
        }
    }
    post {
        always {
            script {
                emailext subject: '$DEFAULT_SUBJECT',
                    body: '$DEFAULT_CONTENT',
                    recipientProviders: [
                        [$class: 'CulpritsRecipientProvider'],
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ],
                    replyTo: '$DEFAULT_REPLYTO'
            }
        }
        success {
            junit 'junit/*.xml'
            cobertura coberturaReportFile: 'coverage.xml'
            //script {
            //    currentBuild.result = 'SUCCESS'
            //}
            //step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck'])
        }
    }
}

def run_pytest(String tests, int timeout, String results, String threads) {
    sh 'echo "<testsuite tests="0"></testsuite>" > junit/' + results + '.xml'
    sh 'py.test ' + tests + ' -rs -n ' + threads + ' --forked --show-progress --cov-config=.coveragerc --cov-branch --cov spynnaker8 --cov spynnaker --cov spinn_front_end_common --cov pacman --cov data_specification --cov spinnman --cov spinn_machine --cov spalloc --cov spinn_utilities --junitxml junit/' + results + '.xml --cov-report xml:coverage.xml --cov-append --timeout ' + timeout + ' --log-level=INFO '
}
