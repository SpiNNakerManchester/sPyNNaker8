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
from spynnaker8.models.populations import Assembly
from p8_integration_tests.base_test_case import BaseTestCase


class Test_Assembly(BaseTestCase):

    def test_simple(self):
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(1, sim.IF_curr_exp(), label="pop_1")
        pop_2 = sim.Population(1, sim.IF_curr_exp(), label="pop_2")
        pop_3 = sim.Population(1, sim.IF_curr_exp(), label="pop_3")
        ass = Assembly(pop_1, pop_2)
        self.assertEquals(2, len(ass))
        ass =+ pop_3
        self.assertEquals(3, len(ass))

