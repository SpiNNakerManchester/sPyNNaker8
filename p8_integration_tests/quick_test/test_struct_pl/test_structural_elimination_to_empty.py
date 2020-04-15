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
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p


def structural_without_stdp():
    p.setup(1.0)
    stim = p.Population(9, p.SpikeSourceArray(range(10)), label="stim")

    # These populations should experience elimination
    pop = p.Population(9, p.IF_curr_exp(), label="pop")

    # Make a full list

    # Elimination with random selection (0 probability formation)
    proj = p.Projection(
        stim, pop, p.AllToAllConnector(),
        p.StructuralMechanismStatic(
            partner_selection=p.RandomSelection(),
            formation=p.DistanceDependentFormation([3, 3], 0.0),
            elimination=p.RandomByWeightElimination(4.0, 1.0, 1.0),
            f_rew=1000, initial_weight=4.0, initial_delay=3.0,
            s_max=9, seed=0, weight=0.0, delay=1.0))

    p.run(1000)

    # Get the final connections
    conns = list(proj.get(["weight", "delay"], "list"))

    p.end()

    # These should have no connections since all should be eliminated
    assert(len(conns) == 0)


class TestStructuralWithoutSTDP(BaseTestCase):

    def test_structural_without_stdp(self):
        self.runsafe(structural_without_stdp)


if __name__ == "__main__":
    structural_without_stdp()
