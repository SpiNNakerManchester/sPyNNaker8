import spynnaker8 as sim
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from p8_integration_tests.base_test_case import BaseTestCase


class ExtractingSpikesWhenVOnlySetToRecord(BaseTestCase):

    def test_cause_error(self):
        with self.assertRaises(ConfigurationException):
            sim.setup(timestep=1.0)
            sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

            pop_1 = sim.Population(1, sim.IF_curr_exp(), label="pop_1")
            input = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]),
                                   label="input")
            sim.Projection(input, pop_1, sim.OneToOneConnector(),
                           synapse_type=sim.StaticSynapse(weight=5, delay=1))
            pop_1.record(["spikes"])
            simtime = 10
            sim.run(simtime)

            pop_1.get_data(variables=["v"])
