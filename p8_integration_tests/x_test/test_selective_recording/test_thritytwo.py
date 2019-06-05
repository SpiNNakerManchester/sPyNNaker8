import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestSampling(BaseTestCase):

    def test_thrtytwo(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

        pop_1 = sim.Population(40, sim.IF_curr_exp(), label="pop_1")
        input = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]),
                               label="input")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=1))
        pop_1.record(["spikes", "v"], indexes=range(32))
        simtime = 10
        sim.run(simtime)

        neo = pop_1.get_data(variables=["spikes", "v"])
        spikes = neo.segments[0].spiketrains
        # Include all the spiketrains as there is no outside index
        self.assertEqualss(40, len(spikes))
        for i in range(32):
            self.assertEqualss(1, len(spikes[i]))
        for i in range(32, 40):
            self.assertEqualss(0, len(spikes[i]))
        v = neo.segments[0].filter(name='v')[0]
        self.assertEqualss(32, len(v.channel_index.index))
        self.assertEqualss(32, len(v[0]))
        sim.end()
