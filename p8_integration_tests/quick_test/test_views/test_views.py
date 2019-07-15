import numpy
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestViews(BaseTestCase):

    def set_with_views(self):
        sim.setup(1.0)
        pop = sim.Population(5, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop[2:4].set(i_offset=2.0)
        pop[1, 3].initialize(v=-60)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        sim.end()
        expected = [
            -65., -64.02465820, -63.09686279, -62.21432495, -61.37481689,
            -60., -59.26849365, -58.57263184, -57.91070557, -57.28106689,
            -65., -63.04931641, -61.19375610, -59.42868042, -57.74966431,
            -60., -58.29315186, -56.66952515, -55.12509155, -53.65597534,
            -65., -64.02465820, -63.09686279, -62.21432495, -61.37481689]
        numpy.allclose(v1[:, 2], expected)

    def test_set_with_views(self):
        self.runsafe(self.set_with_views)
