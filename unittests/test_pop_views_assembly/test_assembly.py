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


class TestAssembly(BaseTestCase):

    def test_simple(self):
        sim.setup(timestep=1.0)
        p1 = sim.Population(1, sim.IF_curr_exp(), label="pop_1")
        p2 = sim.Population(1, sim.IF_curr_exp(), label="pop_2")
        assembly = Assembly(p1, p2, label="simple")
        self.assertEqual(assembly.populations, [p1, p2])
        self.assertEqual(2, len(assembly))
        # Exact string not critical if it looks good
        current_repr = \
            "Assembly(*" \
            "[Population(1, IFCurrExpBase, structure=None, label='pop_1'), " \
            "Population(1, IFCurrExpBase, structure=None, label='pop_2')], " \
            "label='simple')"
        self.assertEqual(current_repr, str(assembly))

    def test___add__two(self, sim=sim):
        # adding two populations should give an Assembly
        sim.setup(timestep=1.0)
        p1 = sim.Population(6, sim.IF_curr_exp())
        p2 = sim.Population(17, sim.IF_cond_exp())
        assembly = p1 + p2
        self.assertIsInstance(assembly, sim.Assembly)
        self.assertEqual(assembly.populations, [p1, p2])

    def test___add__three(self, sim=sim):
        # adding three populations should give an Assembly
        sim.setup(timestep=1.0)
        p1 = sim.Population(6, sim.IF_curr_exp())
        p2 = sim.Population(17, sim.IF_cond_exp())
        p3 = sim.Population(9, sim.IF_cond_exp())
        assembly = p1 + p2 + p3
        self.assertIsInstance(assembly, sim.Assembly)
        self.assertEqual(assembly.populations, [p1, p2, p3])
