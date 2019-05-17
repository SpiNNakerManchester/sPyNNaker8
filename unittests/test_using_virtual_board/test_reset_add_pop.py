import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestResetAdd(BaseTestCase):

    def testReset_add(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 1)

        input = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]), label="input")
        pop_1 = sim.Population(2, sim.IF_curr_exp(), label="pop_1")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        sim.run(10)
        sim.Population(2, sim.IF_curr_exp(), label="pop_2")
        with self.assertRaises(NotImplementedError):
            sim.run(10)
