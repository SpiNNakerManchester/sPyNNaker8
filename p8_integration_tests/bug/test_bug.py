# Copyright (c) 2017-2020 The University of Manchester
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


class TinyTest(BaseTestCase):
    def check_run(self):
        sim.setup(timestep=1.0)
        simtime = 10
        n_neurons = 6
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
        pop_1.record("all")
        sim.run(simtime)

        sim.end()

    def test_run(self):
        self.runsafe(self.check_run)
