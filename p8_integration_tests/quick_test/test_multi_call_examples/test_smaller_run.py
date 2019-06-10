import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.checker import check_data

n_neurons = 20  # number of neurons in each population
neurons_per_core = n_neurons / 2
simtime = 1000


class TestSmaller(BaseTestCase):

    def do_run(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, neurons_per_core)

        input_spikes = list(range(0, simtime - 100, 10))
        expected_spikes = len(input_spikes)
        input = sim.Population(
            1, sim.SpikeSourceArray(spike_times=input_spikes), label="input")
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        pop_1.record(["spikes", "v", "gsyn_exc"])
        sim.run(simtime//4*3)
        sim.run(simtime//4)
        check_data(pop_1, expected_spikes, simtime)
        sim.end()

    def test_do_run(self):
        self.runsafe(self.do_run)
