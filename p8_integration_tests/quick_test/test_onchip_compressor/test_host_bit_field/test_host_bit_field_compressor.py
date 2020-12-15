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

import random
from p8_integration_tests.base_test_case import BaseTestCase
from pacman.model.constraints.placer_constraints import \
    ChipAndCoreConstraint
import spynnaker8 as sim


class TestHostBitFieldCompressor(BaseTestCase):

    def do_run(self):
        random.seed = 1
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_inputs = 10
        n_populations = 10
        n_neurons = 120

        inputs = [
            sim.Population(n_neurons, sim.SpikeSourceArray(spike_times=[0]),
                           label="input_{}".format(i))
            for i in range(n_inputs)
        ]
        pops = [
            sim.Population(1, sim.IF_curr_exp, {}, label='chain_{}'.format(i))
            for i in range(n_populations)
        ]
        for pop in pops:
            pop.set_constraint(ChipAndCoreConstraint(0, 0))

        full_list = []
        for i in range(n_neurons):
            full_list.append([i, 0])
        for i in range(n_inputs):
            for j in range(n_populations):
                sample_list = random.sample(full_list, n_neurons // 2)
                connector = sim.FromListConnector(sample_list)
                sim.Projection(
                    inputs[i], pops[j], connector,
                    synapse_type=sim.StaticSynapse(weight=1, delay=1))
        sim.run(10)

    def test_do_run(self):
        self.runsafe(self.do_run)
