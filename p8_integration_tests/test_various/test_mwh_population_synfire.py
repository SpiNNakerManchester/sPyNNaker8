#!/usr/bin/python
"""
Synfirechain-like example
"""
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from spynnaker8.utilities import neo_convertor
import spynnaker.plot_utils as plot_utils
from spinnman.exceptions import SpinnmanTimeoutException
import unittest
from unittest import SkipTest


def do_run(nNeurons, neurons_per_core):

    p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)
    p.set_number_of_neurons_per_core(p.IF_curr_exp, neurons_per_core)

    nPopulations = 62
    cell_params_lif = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0,
                       'tau_refrac': 2.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
                       'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -50.0}

    populations = list()
    projections = list()

    weight_to_spike = 1.5
    delay = 5

    for i in range(0, nPopulations):
        populations.append(p.Population(nNeurons, p.IF_curr_exp,
                                        cell_params_lif,
                                        label='pop_' + str(i)))
        print "++++++++++++++++"
        print "Added population %s" % (i)
        print "o-o-o-o-o-o-o-o-"
    synapse_type = p.StaticSynapse(weight=weight_to_spike, delay=delay)
    for i in range(0, nPopulations):
        projections.append(p.Projection(populations[i],
                                        populations[(i + 1) % nPopulations],
                                        p.OneToOneConnector(),
                                        synapse_type=synapse_type,
                                        label="Projection from pop {} to pop "
                                              "{}".format(i, (i + 1) %
                                                          nPopulations)))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Added projection from population %s to population %s" \
              % (i, (i + 1) % nPopulations)
        print "----------------------------------------------------"

    from pprint import pprint as pp
    pp(projections)
    spikeArray = {'spike_times': [[0]]}
    populations.append(p.Population(1, p.SpikeSourceArray, spikeArray,
                                    label='inputSpikes_1'))
    projections.append(p.Projection(populations[-1], populations[0],
                                    p.AllToAllConnector(),
                                    synapse_type=synapse_type))

    for i in range(0, nPopulations):
        populations[i].record("v")
        populations[i].record("gsyn_exc")
        populations[i].record("spikes")

    p.run(1500)

    ''''
    weights = projections[0].getWeights()
    delays = projections[0].getDelays()
    '''

    neo = populations[0].get_data(["v", "spikes", "gsyn_exc"])

    v = neo_convertor.convert_data(neo, name="v")
    gsyn = neo_convertor.convert_data(neo, name="gsyn_exc")
    spikes = neo_convertor.convert_spikes(neo)

    p.end()

    return (v, gsyn, spikes)


class MwhPopulationSynfire(BaseTestCase):
    @unittest.skip("Broken p8_integration_tests/test_various/"
                   "test_mwh_population_synfire.py")
    def test_run_heavy(self):
        try:
            nNeurons = 200  # number of neurons in each population
            neurons_per_core = 256
            (v, gsyn, spikes) = do_run(nNeurons, neurons_per_core)
            print len(spikes)
        except SpinnmanTimeoutException as ex:
            raise SkipTest(ex)
        try:
            self.assertLess(580, len(spikes))
            self.assertGreater(620, len(spikes))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)

    def test_run_light(self):
        nNeurons = 200  # number of neurons in each population
        neurons_per_core = 50
        (v, gsyn, spikes) = do_run(nNeurons, neurons_per_core)
        print len(spikes)
        try:
            self.assertLess(580, len(spikes))
            self.assertGreater(620, len(spikes))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)


if __name__ == '__main__':
    nNeurons = 200  # number of neurons in each population
    neurons_per_core = 256
    (v, gsyn, spikes) = do_run(nNeurons, neurons_per_core)
    plot_utils.plot_spikes(spikes)
    plot_utils.line_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
