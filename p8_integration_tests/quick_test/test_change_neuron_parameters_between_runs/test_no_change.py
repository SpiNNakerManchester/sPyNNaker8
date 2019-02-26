import spynnaker8 as sim
from unittest import SkipTest
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoChange(BaseTestCase):

    def check_v(self, v):
        assert v[0][2] == -65.
        assert v[1][2] == -64.024658203125
        assert v[2][2] == -63.09686279296875
        assert v[3][2] == -62.214324951171875
        assert v[4][2] == -61.37481689453125

    def test_change_nothing(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        self.check_v(v1)
        sim.reset()
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()

    def test_change_pre_reset(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        self.check_v(v1)
        pop.set(tau_syn_E=1)
        sim.reset()
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        try:
            self.check_v(v2)
        except AssertionError:
            self.report("https://github.com/SpiNNakerManchester/sPyNNaker"
                        "/issues/599\n", "Skipped_due_to_issue")
            raise SkipTest("https://github.com/SpiNNakerManchester/sPyNNaker"
                        "/issues/599")
        sim.end()

    def test_change_post_set(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        self.check_v(v1)
        sim.reset()
        pop.set(tau_syn_E=1)
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()
