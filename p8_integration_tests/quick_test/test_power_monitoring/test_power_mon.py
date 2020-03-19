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

import numpy
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
run_times = [5000, 5000]
# parameters for population 1 first run
input_class = p.SpikeSourcePoisson
start_time = 0
duration = 5000.0
rate = 2.0
# parameters for population 2 first run
set_between_runs = [(1, 'start', 5000),
                    (1, 'rate', 200.0),
                    (1, 'duration', 2000.0)]
extract_between_runs = False
synfire_run = SynfireRunner()


class TestPowerMonitoring(BaseTestCase):
    def do_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=run_times, input_class=input_class,
                           start_time=start_time, duration=duration, rate=rate,
                           extract_between_runs=extract_between_runs,
                           set_between_runs=set_between_runs,
                           seed=12345)
        spikes = synfire_run.get_output_pop_spikes_numpy()
        self.assertIsNotNone(spikes, "must have some spikes")
        # Check spikes increase in second half by at least a factor of ten
        hist = numpy.histogram(spikes[:, 1], bins=[0, 5000, 10000])
        self.assertIsNotNone(hist, "must have a histogram")
        # TODO: Test that the power info is in the reports
        # TODO: Test that the power info is in the provenance

    def test_power_monitoring(self):
        self.runsafe(self.do_run)
