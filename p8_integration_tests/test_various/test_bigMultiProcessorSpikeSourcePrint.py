"""
Synfirechain-like example
"""
# !/usr/bin/python
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker.plot_utils as plot_utils


def do_run(nNeurons, neurons_per_core):
    cell_params_lif = {'cm': 0.25,  # nF
                       'i_offset': 0.0,
                       'tau_m': 10.0,
                       'tau_refrac': 2.0,
                       'tau_syn_E': 2.5,
                       'tau_syn_I': 2.5,
                       'v_reset': -70.0,
                       'v_rest': -65.0,
                       'v_thresh': -55.4
                       }

    spike_list = {'spike_times': [float(x) for x in range(0, 599, 50)]}
    p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)

    p.set_number_of_neurons_per_core(p.SpikeSourceArray, neurons_per_core)

    populations = list()
    projections = list()

    populations.append(p.Population(nNeurons, p.SpikeSourceArray, spike_list,
                                    label='input'))
    populations.append(p.Population(1, p.IF_curr_exp, cell_params_lif,
                                    label='pop_1'))
    projections.append(p.Projection(populations[0], populations[1],
                                    p.AllToAllConnector()))

    populations[0].record("spikes")

    p.run(1000)

    neo = populations[0].get_data("spikes")

    p.end()

    return neo


class BigMultiProcessorSpikeSourcePrint(BaseTestCase):

    def test_sixty(self):
        nNeurons = 600  # number of neurons in each population
        neo = do_run(nNeurons, 60)
        spike_count = neo_convertor.count_spikes(neo)
        self.assertEquals(spike_count, 7200)

    def test_seventy(self):
        nNeurons = 600  # number of neurons in each population
        neo = do_run(nNeurons, 70)
        spike_count = neo_convertor.count_spikes(neo)
        self.assertEquals(spike_count, 7200)


if __name__ == '__main__':
    nNeurons = 600  # number of neurons in each population
    neo = do_run(nNeurons, 60)
    spikes = neo_convertor.convert_spikes(neo)
    plot_utils.plot_spikes(spikes)
    print spikes

    neo = do_run(nNeurons, 70)
    spikes = neo_convertor.convert_spikes(neo)
    plot_utils.plot_spikes(spikes)
    print spikes
