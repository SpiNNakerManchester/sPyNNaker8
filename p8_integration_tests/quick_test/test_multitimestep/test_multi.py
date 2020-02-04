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

from __future__ import division
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.quick_test.test_multitimestep.\
    multi_if_curr_exp_base import MultiIFCurrExpBase


class TestMulti(BaseTestCase):

    def do_multi(self):
        sim.setup(timestep=1)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 3)
        input = sim.Population(
            1, sim.SpikeSourceArray([4]), label="input",
            additional_parameters={"timestep_in_us": 2200}
        )
        input.record("spikes")
        pop_1 = sim.Population(9, MultiIFCurrExpBase(), label="pop_1")
        pop_1.record(["spikes", "v"])

        proj = sim.Projection(
            input, pop_1, sim.AllToAllConnector(),
            synapse_type=sim.StaticSynapse(weight=5, delay=6))
        sim.run(33)

        proj.get("delay", "list")
        i_neo = input.get_data(variables=["spikes"])
        i_spikes = i_neo.segments[0].spiketrains
        print(i_spikes)

        neo = pop_1.get_data(variables="all")
        spikes = neo.segments[0].spiketrains
        print(spikes)
        v = neo.segments[0].filter(name='v')[0]
        print(v)
        sim.end()

    def test_multi(self):
        self.runsafe(self.do_multi)
