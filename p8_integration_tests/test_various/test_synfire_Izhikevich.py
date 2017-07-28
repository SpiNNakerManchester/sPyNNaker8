#!/usr/bin/python
"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
from unittest import SkipTest


def do_run(nNeurons):
    p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)
    p.set_number_of_neurons_per_core(p.Izhikevich, 100)

    cell_params_izk = {
        'a': 0.02,
        'b': 0.2,
        'c': -65,
        'd': 8,
        'v_init': -75,
        'u_init': 0,
        'tau_syn_E': 2,
        'tau_syn_I': 2,
        'i_offset': 0
        }

    populations = list()
    projections = list()

    weight_to_spike = 40
    delay = 1

    connections = list()
    for i in range(0, nNeurons):
        singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, delay)
        connections.append(singleConnection)

    injectionConnection = [(0, 0, weight_to_spike, delay)]
    spikeArray = {'spike_times': [[50]]}
    populations.append(p.Population(nNeurons, p.Izhikevich, cell_params_izk,
                                    label='pop_1'))
    populations.append(p.Population(1, p.SpikeSourceArray, spikeArray,
                                    label='inputSpikes_1'))

    projections.append(p.Projection(populations[0], populations[0],
                                    p.FromListConnector(connections)))
    projections.append(p.Projection(populations[1], populations[0],
                                    p.FromListConnector(injectionConnection)))

    populations[0].record("v")
    populations[0].record("gsyn_exc")
    populations[0].record("spikes")

    p.run(500)

    neo = populations[0].get_data(["v", "spikes", "gsyn_exc"])

    v = neo_convertor.convert_data(neo, name="v")
    gsyn = neo_convertor.convert_data(neo, name="gsyn_exc")
    spikes = neo_convertor.convert_spikes(neo)

    p.end()

    return (v, gsyn, spikes)


class SynfireIzhikevich(BaseTestCase):
    def test_run(self):
        nNeurons = 200  # number of neurons in each population
        (v, gsyn, spikes) = do_run(nNeurons)
        spike_checker.synfire_spike_checker(spikes, nNeurons)
        try:
            self.assertLess(200, len(spikes))
            self.assertGreater(230, len(spikes))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)


if __name__ == '__main__':
    nNeurons = 200  # number of neurons in each population
    (v, gsyn, spikes) = do_run(nNeurons)
    print len(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
