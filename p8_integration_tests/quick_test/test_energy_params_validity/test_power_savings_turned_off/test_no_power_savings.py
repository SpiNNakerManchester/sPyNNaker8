from testfixtures import LogCapture
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class Synfire2RunExtractionIfCurrExp(BaseTestCase):
    def test_run(self):
        with LogCapture() as lc:
            sim.setup(1.0)
            pop = sim.Population(1, sim.IF_curr_exp, {}, label="pop")
            inp = sim.Population(1, sim.SpikeSourceArray(
                spike_times=[0]), label="input")
            sim.Projection(inp, pop, sim.OneToOneConnector(),
                           synapse_type=sim.StaticSynapse(weight=5))
            sim.run(10)
            self.assert_logs_messages(
                lc.records, "Working out if machine is booted", 'INFO', 1)