import spynnaker8 as sim
from spynnaker8.utilities import neo_compare
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.checker import check_neuron_data

n_neurons = 20  # number of neurons in each population
neurons_per_core = n_neurons / 2
simtime = 200


class TestResetNewInput(BaseTestCase):

    def check_data(self, pop, expected_spikes, simtime, segment):
        neo = pop.get_data("all")
        spikes = neo.segments[segment].spiketrains
        v = neo.segments[segment].filter(name="v")[0]
        gsyn_exc = neo.segments[segment].filter(name="gsyn_exc")[0]
        for i in range(len(spikes)):
            check_neuron_data(spikes[i], v[:, i], gsyn_exc[:, i],
                              expected_spikes,
                              simtime, pop.label, i)

    def do_run(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, neurons_per_core)

        input_spikes1 = list(range(0, simtime - 50, 10))
        input = sim.Population(
            1, sim.SpikeSourceArray(spike_times=input_spikes1), label="input")
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        pop_1.record(["spikes", "v", "gsyn_exc"])
        sim.run(simtime)
        sim.reset()
        input_spikes2 = list(range(0, simtime - 50, 11))
        input.set(spike_times=input_spikes2)
        sim.run(simtime)
        self.check_data(pop_1, len(input_spikes1), simtime, 0)
        self.check_data(pop_1, len(input_spikes2), simtime, 1)
        sim.end()

    def test_do_run(self):
        self.runsafe(self.do_run)
