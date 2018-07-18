import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import numpy
import math
import unittest


class TestIFCondExpSTDPPairAdditive(BaseTestCase):

    def test_potentiation_and_depression(self):
        p.setup(1)
        runtime = 100
        initial_run = 1000  # to negate any initial conditions

        # STDP parameters
        a_plus = 0.1
        a_minus = 0.0375
        tau_plus = 20
        tau_minus = 64
        plastic_delay = 1
        initial_weight = 0.05
        max_weight = 0.1
        min_weight = 0

        spike_times = [10, 50]
        spike_times2 = [30]

        for i in range(len(spike_times)):
            spike_times[i] += initial_run

        for i in range(len(spike_times2)):
            spike_times2[i] += initial_run

        # Spike source to send spike via plastic synapse
        pop_src1 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        pop_src2 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times2}, label="src2")

        # Post-plastic-synapse population
        pop_exc = p.Population(1, p.IF_cond_exp(),  label="test")

        # Create projections
        p.Projection(
            pop_src1, pop_exc, p.OneToOneConnector(),
            p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

        p.Projection(
            pop_src2, pop_exc, p.OneToOneConnector(),
            p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

        syn_plas = p.STDPMechanism(
            timing_dependence=p.SpikePairRule(tau_plus=tau_plus,
                                              tau_minus=tau_minus,
                                              A_plus=a_plus, A_minus=a_minus),
            weight_dependence=p.AdditiveWeightDependence(w_min=min_weight,
                                                         w_max=max_weight),
            weight=initial_weight, delay=plastic_delay)

        plastic_synapse = p.Projection(pop_src1, pop_exc,
                                       p.OneToOneConnector(),
                                       synapse_type=syn_plas,
                                       receptor_type='excitatory')

        pop_src1.record('all')
        pop_exc.record("all")
        p.run(initial_run + runtime)
        weights = []

        weights.append(plastic_synapse.get('weight', 'list',
                                           with_address=False)[0])

        # pre_spikes = pop_src1.get_data('spikes')
        # v = pop_exc.get_data('v')
        spikes = pop_exc.get_data('spikes')

        potentiation_time_1 = (spikes.segments[0].spiketrains[0].magnitude[0] +
                               plastic_delay) - spike_times[0]
        potentiation_time_2 = (spikes.segments[0].spiketrains[0].magnitude[1] +
                               plastic_delay) - spike_times[0]

        depression_time_1 = spike_times[1] - (
            spikes.segments[0].spiketrains[0].magnitude[0] + plastic_delay)
        depression_time_2 = spike_times[1] - (
            spikes.segments[0].spiketrains[0].magnitude[1] + plastic_delay)

        potentiation_1 = max_weight * a_plus * \
            math.exp(-potentiation_time_1/tau_plus)
        potentiation_2 = max_weight * a_plus * \
            math.exp(-potentiation_time_2/tau_plus)

        depression_1 = max_weight * a_minus * \
            math.exp(-depression_time_1/tau_minus)
        depression_2 = max_weight * a_minus * \
            math.exp(-depression_time_2/tau_minus)

        new_weight_exact = (initial_weight + potentiation_1 + potentiation_2
                            - depression_1 - depression_2)

        print("Pre neuron spikes at: {}".format(spike_times))
        print("Post-neuron spikes at: {}".format(
            spikes.segments[0].spiketrains[0].magnitude))
        print("Potentiation time differences: {}, {},\
             \nDepression time difference: {}, {}".format(
                 potentiation_time_1, potentiation_time_2,
                 depression_time_1, depression_time_2))
        print("Ammounts to potentiate: {}, {},\
            \nAmount to depress: {}, {},".format(
                potentiation_1, potentiation_2, depression_1, depression_2))
        print("New weight exact: {}".format(new_weight_exact))
        print("New weight SpiNNaker: {}".format(weights[0]))

        self.assertTrue(numpy.allclose(weights[0],
                                       new_weight_exact, rtol=0.001))
        p.end()


if __name__ == '__main__':
    unittest.main()
