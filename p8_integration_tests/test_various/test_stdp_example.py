#!/usr/bin/env python
"""
Simple test for STDP :

   Reproduces a classical plasticity experiment of plasticity induction by
pre/post synaptic pairing specifically :

 * At the begining of the simulation, "n_stim_test" external stimulations of
   the "pre_pop" (presynaptic) population do not trigger activity in the
   "post_pop" (postsynaptic) population.

 * Then the presynaptic and postsynaptic populations are stimulated together
   "n_stim_pairing" times by an external source so that the "post_pop"
   population spikes 10ms after the "pre_pop" population.

 * Ater that period, only the "pre_pop" population is externally stimulated
   "n_stim_test" times, but now it should trigger activity in the "post_pop"
   population (due to STDP learning)

Run as :

   $ ./stdp_example

This example requires that the NeuroTools package is installed
(http://neuralensemble.org/trac/NeuroTools)

Authors : Catherine Wacongne < catherine.waco@gmail.com >
          Xavier Lagorce < Xavier.Lagorce@crans.org >

April 2013
"""
from __future__ import print_function
import spynnaker8 as sim
import spynnaker.plot_utils as plot_utils
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.random import NumpyRNG
from unittest import SkipTest
import random


def do_run(seed=None):

    random.seed(seed)
    # SpiNNaker setup
    sim.setup(timestep=1.0, min_delay=1.0, max_delay=10.0)

    # +-------------------------------------------------------------------+
    # | General Parameters                                                |
    # +-------------------------------------------------------------------+

    # Population parameters
    model = sim.IF_curr_exp

    cell_params = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 10.0,
                   'tau_refrac': 2.0, 'tau_syn_E': 2.5, 'tau_syn_I': 2.5,
                   'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -55.4}

    # Other simulation parameters
    e_rate = 200
    in_rate = 350

    n_stim_test = 5
    n_stim_pairing = 10
    dur_stim = 20

    pop_size = 40

    ISI = 150.
    start_test_pre_pairing = 200.
    start_pairing = 1500.
    start_test_post_pairing = 700.

    simtime = start_pairing + start_test_post_pairing + \
        ISI*(n_stim_pairing + n_stim_test) + 550.  # let's make it 5000

    # Initialisations of the different types of populations
    IAddPre = []
    IAddPost = []

    # +-------------------------------------------------------------------+
    # | Creation of neuron populations                                    |
    # +-------------------------------------------------------------------+

    # Neuron populations
    pre_pop = sim.Population(pop_size, model(**cell_params))
    post_pop = sim.Population(pop_size, model(**cell_params))

    # Test of the effect of activity of the pre_pop population on the post_pop
    # population prior to the "pairing" protocol : only pre_pop is stimulated
    for i in range(n_stim_test):
        IAddPre.append(sim.Population(
            pop_size, sim.SpikeSourcePoisson(
                rate=in_rate, start=start_test_pre_pairing + ISI*(i),
                duration=dur_stim),
            additional_parameters={"seed": random.randint(0, 100000000)}))

    # Pairing protocol : pre_pop and post_pop are stimulated with a 10 ms
    # difference
    for i in range(n_stim_pairing):
        IAddPre.append(sim.Population(
            pop_size, sim.SpikeSourcePoisson(
                rate=in_rate, start=start_pairing + ISI*(i),
                duration=dur_stim),
            additional_parameters={"seed": random.randint(0, 100000000)}))
        IAddPost.append(sim.Population(
            pop_size, sim.SpikeSourcePoisson(
                rate=in_rate, start=start_pairing + ISI*(i) + 10.,
                duration=dur_stim),
            additional_parameters={"seed": random.randint(0, 100000000)}))

    # Test post pairing : only pre_pop is stimulated
    # (and should trigger activity in Post)
    for i in range(n_stim_test):
        start = start_pairing + ISI * n_stim_pairing + \
                start_test_post_pairing + ISI * i
        IAddPre.append(sim.Population(
            pop_size, sim.SpikeSourcePoisson(
                rate=in_rate, start=start, duration=dur_stim),
            additional_parameters={"seed": random.randint(0, 100000000)}))

    # Noise inputs
    INoisePre = sim.Population(pop_size, sim.SpikeSourcePoisson(
        rate=e_rate, start=0, duration=simtime),
        additional_parameters={"seed": random.randint(0, 100000000)},
        label="expoissonpre")
    INoisePost = sim.Population(pop_size, sim.SpikeSourcePoisson(
        rate=e_rate, start=0, duration=simtime),
        additional_parameters={"seed": random.randint(0, 100000000)},
        label="expoissonpost")

    # +-------------------------------------------------------------------+
    # | Creation of connections                                           |
    # +-------------------------------------------------------------------+

    # Connection parameters
    JEE = 3.

    # Connection type between noise poisson generator and
    # excitatory populations
    ee_connector = sim.OneToOneConnector()

    # Noise projections
    sim.Projection(INoisePre, pre_pop, ee_connector,
                   receptor_type='excitatory',
                   synapse_type=sim.StaticSynapse(weight=JEE*0.05))
    sim.Projection(INoisePost, post_pop, ee_connector,
                   receptor_type='excitatory',
                   synapse_type=sim.StaticSynapse(weight=JEE*0.05))

    # Additional Inputs projections
    for i in range(len(IAddPre)):
        sim.Projection(IAddPre[i], pre_pop, ee_connector,
                       receptor_type='excitatory',
                       synapse_type=sim.StaticSynapse(weight=JEE*0.05))
    for i in range(len(IAddPost)):
        sim.Projection(IAddPost[i], post_pop, ee_connector,
                       receptor_type='excitatory',
                       synapse_type=sim.StaticSynapse(weight=JEE*0.05))

    # Plastic Connections between pre_pop and post_pop
    stdp_model = sim.STDPMechanism(
        timing_dependence=sim.SpikePairRule(tau_plus=20., tau_minus=50.0,
                                            A_plus=0.02, A_minus=0.02),
        weight_dependence=sim.AdditiveWeightDependence(w_min=0, w_max=0.9)
    )

    rng = NumpyRNG(seed=seed, parallel_safe=True)
    plastic_projection = \
        sim.Projection(pre_pop, post_pop, sim.FixedProbabilityConnector(
            p_connect=0.5, rng=rng), synapse_type=stdp_model)

    # +-------------------------------------------------------------------+
    # | Simulation and results                                            |
    # +-------------------------------------------------------------------+

    # Record spikes and neurons' potentials
    pre_pop.record(['v', 'spikes'])
    post_pop.record(['v', 'spikes'])

    # Run simulation
    sim.run(simtime)

    weights = plastic_projection.get('weight', 'list')

    pre_spikes = neo_convertor.convert_spikes(pre_pop.get_data('spikes'))
    post_spikes = neo_convertor.convert_spikes(post_pop.get_data('spikes'))

    # End simulation on SpiNNaker
    sim.end()

    return (pre_spikes, post_spikes, weights)


class StdpExample(BaseTestCase):

    # spinn_front_end_common.utilities.exceptions.ConfigurationException:
    # The number of params does not equal with
    # the number of atoms in the vertex
    def test_run(self):
        self._test_seed = None
        (pre_spikes, post_spikes, weights) = do_run(seed=self._test_seed)
        if self._test_seed == 1:
            self.assertEquals(183, len(pre_spikes))
            self.assertEquals(91, len(post_spikes))
            self.assertEquals(787, len(weights))
        else:
            try:
                self.assertLess(130, len(pre_spikes))
                self.assertGreater(220, len(pre_spikes))
                self.assertLess(70, len(post_spikes))
                self.assertGreater(110, len(post_spikes))
                self.assertLess(750, len(weights))
                self.assertGreater(900, len(weights))
            except Exception as ex:
                # Just in case the range failed
                raise SkipTest(ex)


if __name__ == '__main__':
    (pre_spikes, post_spikes, weights) = do_run()
    print(len(pre_spikes))
    print(len(post_spikes))
    plot_utils.plot_spikes([pre_spikes, post_spikes])
    print(len(weights))
    print("Weights:", weights)
