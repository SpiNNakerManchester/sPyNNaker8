import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import numpy
import unittest


class TestSTDPPairAdditive(BaseTestCase):

    def test_potentiation_and_depression(self):
        p.setup(1)
        runtime = 100
        initial_run = 1000  # to negate any initial conditions

        # STDP parameters
        a_plus = 0.01
        a_minus = 0.01
        tau_plus = 20
        tau_minus = 20
        plastic_delay = 3
        initial_weight = 2.5
        max_weight = 5
        min_weight = 0

        pre_spikes = [10, 50]
        extra_spikes = [30]

        for i in range(len(pre_spikes)):
            pre_spikes[i] += initial_run

        for i in range(len(extra_spikes)):
            extra_spikes[i] += initial_run

        # Spike source to send spike via plastic synapse
        pre_pop = p.Population(1, p.SpikeSourceArray,
                               {'spike_times': pre_spikes}, label="pre")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        extra_pop = p.Population(1, p.SpikeSourceArray,
                                 {'spike_times': extra_spikes}, label="extra")

        # Post-plastic-synapse population
        post_pop = p.Population(1, p.IF_curr_exp(),  label="post")

        # Create projections
        p.Projection(
            pre_pop, post_pop, p.OneToOneConnector(),
            p.StaticSynapse(weight=5.0, delay=1), receptor_type="excitatory")

        p.Projection(
            extra_pop, post_pop, p.OneToOneConnector(),
            p.StaticSynapse(weight=5.0, delay=1), receptor_type="excitatory")

        syn_plas = p.STDPMechanism(
            timing_dependence=p.SpikePairRule(tau_plus=tau_plus,
                                              tau_minus=tau_minus,
                                              A_plus=a_plus, A_minus=a_minus),
            weight_dependence=p.AdditiveWeightDependence(w_min=min_weight,
                                                         w_max=max_weight),
            weight=initial_weight, delay=plastic_delay)

        plastic_synapse = p.Projection(pre_pop, post_pop,
                                       p.OneToOneConnector(),
                                       synapse_type=syn_plas,
                                       receptor_type='excitatory')

        # Record the spikes
        post_pop.record("spikes")

        # Run
        p.run(initial_run + runtime)

        # Get the weights
        weights = plastic_synapse.get('weight', 'list',
                                      with_address=False)

        # Get the spikes
        post_spikes = numpy.array(
            post_pop.get_data('spikes').segments[0].spiketrains[0].magnitude)

        # End the simulation as all information gathered
        p.end()

        # Get the spikes and time differences that will be considered by
        # the simulation (as the last pre-spike will be considered differently)
        last_pre_spike = pre_spikes[-1]
        considered_post_spikes = post_spikes[post_spikes < last_pre_spike]
        potentiation_time_diff = numpy.ravel(numpy.subtract.outer(
            considered_post_spikes + plastic_delay, pre_spikes[:-1]))
        potentiation_times = (
            potentiation_time_diff[potentiation_time_diff > 0] * -1)
        depression_time_diff = numpy.ravel(numpy.subtract.outer(
            considered_post_spikes + plastic_delay, pre_spikes))
        depression_times = depression_time_diff[depression_time_diff < 0]

        # Work out the weight according to the rules
        potentiations = max_weight * a_plus * numpy.exp(
            (potentiation_times / tau_plus))
        depressions = max_weight * a_minus * numpy.exp(
            (depression_times / tau_minus))
        new_weight_exact = \
            initial_weight + numpy.sum(potentiations) - numpy.sum(depressions)

        print("Pre neuron spikes at: {}".format(pre_spikes))
        print("Post-neuron spikes at: {}".format(post_spikes))
        target_spikes = [1014,  1032, 1053]
        self.assertListEqual(list(post_spikes), target_spikes)
        print("Potentiation time differences: {}".format(potentiation_times))
        print("Depression time differences: {}".format(depression_times))
        print("Potentiation: {}".format(potentiations))
        print("Depressions: {}".format(depressions))
        print("New weight exact: {}".format(new_weight_exact))
        print("New weight SpiNNaker: {}".format(weights))

        self.assertTrue(numpy.allclose(weights, new_weight_exact, rtol=0.001))

    def test_potentiation_and_depression(self):
        self.runsafe(self.potentiation_and_depression)


if __name__ == '__main__':
    unittest.main()
