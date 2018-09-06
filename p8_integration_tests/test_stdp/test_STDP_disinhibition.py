import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import numpy
import math
import unittest


class TestSTDPNearestPairAdditive(BaseTestCase):

    def test_potentiation_and_depression(self):
        p.setup(1)
        runtime = 1000
        initial_run = 1000  # to negate any initial conditions
        n_inhib_neurons = 25
        n_repeats = 10

        # STDP parameters
        a_plus = 0.1
        a_minus = 0.0
        tau_plus = 2
        tau_minus = 5
        plastic_delay = 1
        initial_weight = 1
        max_weight = 5
        min_weight = 0

        spike_times = [[x, x+(runtime/2)] for x in range(n_inhib_neurons)]
        spike_times2 = [15]  # range(10, 1000, 100)

        for i in range(len(spike_times)):
            spike_times[i][0] += initial_run
            spike_times[i][1] += initial_run

        for i in range(len(spike_times2)):
            spike_times2[i] += initial_run

        # Spike source to send spike via plastic synapse
        pop_src1 = p.Population(n_inhib_neurons, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        pop_src2 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times2}, label="src2")

        # Post-plastic-synapse population
        neuron_params= {'tau_refrac': 10}
        pop_exc = p.Population(1, p.IF_curr_exp(**neuron_params),  label="test")

        # Create projections
#         p.Projection(
#             pop_src1, pop_exc, p.AllToAllConnector(),
#             p.StaticSynapse(weight=5.0, delay=1), receptor_type="excitatory")

        p.Projection(
            pop_src2, pop_exc, p.OneToOneConnector(),
            p.StaticSynapse(weight=30.0, delay=1), receptor_type="excitatory")

        syn_plas = p.STDPMechanism(
                                timing_dependence=p.SpikePairRule(A_plus=a_plus, A_minus=a_minus,
                                                                  tau_plus=tau_plus, tau_minus=tau_minus),
                                weight_dependence=p.AdditiveWeightDependence(
                                    w_min=min_weight, w_max=max_weight),
                                weight=initial_weight, delay=plastic_delay)

        plastic_synapse = p.Projection(pop_src1, pop_exc,
                                       p.AllToAllConnector(),
                                       synapse_type=syn_plas,
                                       receptor_type="inhibitory")

        pop_src1.record('all')
        pop_exc.record("all")
        p.run(initial_run + runtime)
        weights = []

        weights.append(plastic_synapse.get(attribute_names=['weight'], format='list', with_address=False))

        # pre_spikes = pop_src1.get_data('spikes')
        # v = pop_exc.get_data('v')
        print weights
        spikes = pop_exc.get_data('spikes')

        potentiation_time = (spikes.segments[0].spiketrains[0].magnitude[0] +
                             plastic_delay) - spike_times[0]
        depression_time = spike_times[1] - (
            spikes.segments[0].spiketrains[0].magnitude[1] + plastic_delay)

        potentiation = max_weight * a_plus * \
            math.exp(-potentiation_time/tau_plus)
        depression = max_weight * a_minus * \
            math.exp(-depression_time/tau_minus)
        new_weight_exact = (initial_weight + potentiation - depression)

        print("Pre neuron spikes at: {}".format(spike_times))
        print("Post-neuron spikes at: {}".format(
            spikes.segments[0].spiketrains[0].magnitude))
        print("Potentiation time difference: {},\
             \nDepression time difference: {}".format(
            potentiation_time, depression_time))
        print("Ammount to potentiate: {}, \
            \nAmount to depress: {}".format(
            potentiation, depression))
        print("New weight exact: {}".format(new_weight_exact))
        print("New weight SpiNNaker: {}".format(weights[0]))

        self.assertTrue(numpy.allclose(
                        weights[0], new_weight_exact, atol=0.001))
        p.end()


if __name__ == '__main__':
    unittest.main()
