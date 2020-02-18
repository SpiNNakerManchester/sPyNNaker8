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

def run_pytest(String tests, int timeout, String results, String threads) {
    sh 'echo "<testsuite tests="0"></testsuite>" > junit/' + results + '.xml'
    sh 'py.test ' + tests + ' -rs -n ' + threads + ' --forked --show-progress --cov-branch --cov spynnaker8 --cov spynnaker --cov spinn_front_end_common --cov pacman --cov data_specification --cov spinnman --cov spinn_machine --cov spinn_storage_handlers --cov spalloc --cov spinn_utilities --junitxml junit/' + results + '.xml --cov-report xml:coverage.xml --cov-append --timeout ' + timeout
}

def clean_and_checkout() {
    sh 'rm -rf ${WORKSPACE}/*'
    sh 'rm -rf ${WORKSPACE}/.[a-zA-Z0-9]*'
    dir('sPyNNaker8') {
        checkout scm
    }
}
