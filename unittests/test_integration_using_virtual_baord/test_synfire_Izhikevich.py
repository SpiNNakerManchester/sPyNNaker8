#!/usr/bin/python
"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as p


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

    p.end()

    return neo


class SynfireIzhikevich(BaseTestCase):
    def test_run(self):
        nNeurons = 200  # number of neurons in each population
        do_run(nNeurons)


if __name__ == '__main__':
    nNeurons = 200  # number of neurons in each population
    do_run(nNeurons)
