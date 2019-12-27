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

import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase

class TestSimpleSsaSpecial(BaseTestCase):

    def do_run(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

        pop_1 = sim.Population(1, sim.IF_curr_exp(), label="pop_1")
        input = sim.Population(1, sim.SpikeSourceArray(), label="input")
        # Hack in a different timestep
        input._vertex._timestep_in_us = 3000
        # Spiketimes must be provided after hacked timestep
        input._vertex.spike_times = [5]
        input.record("spikes")
        sim.Projection(input, pop_1, sim.OneToOneConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        pop_1.record(["spikes", "v"])
        simtime = 20
        sim.run(simtime)

        neo = input.get_data(variables=["spikes"])
        i_spikes = neo.segments[0].spiketrains
        self.assertEquals(len(i_spikes), 1)
        # 5 is rounded up to 6
        self.assertEquals(i_spikes[0].magnitude, 6)
        neo = pop_1.get_data(variables=["spikes", "v"])
        spikes = neo.segments[0].spiketrains
        # Spike sent timestgep after the 6 so 9. Pop spikes 6 steps later so 15
        self.assertEquals(spikes[0].magnitude, 15)
        v = neo.segments[0].filter(name='v')[0]
        # Runtime 20ms rounded up to next lcm timestep of 3000us so 21ms
        self.assertEquals(v.size, 21)
        print("Ran for {} timesteps".format(v.size))
        sim.end()

    def test_do_run(self):
        self.runsafe(self.do_run)
