import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestSpikeSourceArrayGetData(BaseTestCase):

    def do_run(self):
        p.setup(timestep=1, min_delay=1, max_delay=15)

        population = p.Population(1, p.SpikeSourceArray(spike_times=[[0]]),
                                  label='inputSSA_1')

        population.record("all")

        p.run(30)
        neo = population.get_data("all")
        p.end()

    def test_run(self):
        self.runsafe(self.do_run)
