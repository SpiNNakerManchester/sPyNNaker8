import spynnaker8 as sim
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
            self.known_issue(
                "https://github.com/SpiNNakerManchester/sPyNNaker")
        sim.end()

    def test_run_set_run_reset(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(2)
        pop.set(tau_syn_E=1)
        sim.run(3)
        v1 = pop.spinnaker_get_data('v')
        self.check_v(v1)
        sim.reset()

        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()
        print(v1)
        print(v2)

    def test_run_set_run_reset_set(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(2)
        pop.set(tau_syn_E=1)
        sim.run(3)
        v1 = pop.spinnaker_get_data('v')
        self.check_v(v1)

        sim.reset()
        pop.set(tau_syn_E=1)
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        try:
            self.check_v(v2)
        except AssertionError:
            self.known_issue(
                "https://github.com/SpiNNakerManchester/sPyNNaker")
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

    def test_no_change_v(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        inp = sim.Population(1, sim.SpikeSourceArray(
            spike_times=[0]), label="input")
        sim.Projection(inp, pop, sim.OneToOneConnector(),
                     synapse_type=sim.StaticSynapse(weight=5))
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        sim.reset()
        inp.set(spike_times=[100])
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()

    def test_change_v_before(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        inp = sim.Population(1, sim.SpikeSourceArray(
            spike_times=[0]), label="input")
        sim.Projection(inp, pop, sim.OneToOneConnector(),
                     synapse_type=sim.StaticSynapse(weight=5))
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        pop.initialize(v=-65)
        sim.reset()
        inp.set(spike_times=[100])
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()

    def test_change_v_after(self):
        sim.setup(1.0)
        pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
        inp = sim.Population(1, sim.SpikeSourceArray(
            spike_times=[0]), label="input")
        sim.Projection(inp, pop, sim.OneToOneConnector(),
                     synapse_type=sim.StaticSynapse(weight=5))
        pop.set(i_offset=1.0)
        pop.set(tau_syn_E=1)
        pop.record(["v"])
        sim.run(5)
        v1 = pop.spinnaker_get_data('v')
        sim.reset()
        pop.initialize(v=-65)
        inp.set(spike_times=[100])
        sim.run(5)
        v2 = pop.spinnaker_get_data('v')
        self.check_v(v2)
        sim.end()
