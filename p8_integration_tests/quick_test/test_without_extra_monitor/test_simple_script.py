import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestSimpleScript(BaseTestCase):

    def simple_script(self):
        # A simple script that should work whatever we do, but only if the
        # SDRAM is worked out correctly!
        p.setup(1.0)
        src = p.Population(1, p.SpikeSourceArray([50, 150]), label="input_pop")
        pop = p.Population(1, p.IF_curr_exp(), label="neuron")
        p.Projection(
            src, pop, p.OneToOneConnector(),
            synapse_type=p.StaticSynapse(weight=1.0))
        src.record('spikes')
        pop.record("all")
        p.run(200)
        p.end()

    def test_simple_script(self):
        self.runsafe(self.simple_script)
