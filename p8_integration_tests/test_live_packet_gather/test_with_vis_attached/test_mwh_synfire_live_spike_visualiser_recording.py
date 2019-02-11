"""
Synfirechain-like example
"""
# !/usr/bin/python
from pacman.model.constraints.placer_constraints import (
    ChipAndCoreConstraint)
import spynnaker.spike_checker as spike_checker
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase

# number of neurons in each population
nNeurons = 10


def do_run():
    # p.setup(timestep=1.0, min_delay = 1.0, max_delay = 32.0)
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    # max_delay = 50
    # p.set_number_of_neurons_per_core("IF_curr_exp", nNeurons / 2)
    # p.set_number_of_neurons_per_core("DelayExtension", nNeurons / 2)

    cell_params_lif = {'cm': 0.25,  # nF
                       'i_offset': 0.0,
                       'tau_m': 20.0,
                       'tau_refrac': 2.0,
                       'tau_syn_E': 5.0,
                       'tau_syn_I': 5.0,
                       'v_reset': -70.0,
                       'v_rest': -65.0,
                       'v_thresh': -50.0
                       }

    populations = list()
    projections = list()

    weight_to_spike = 2.0
    # d_value = 3.1
    delay = 3
    # delay = numpy.random.RandomState()
    delays = list()

    connections = list()
    for i in range(0, nNeurons):
        # d_value = int(delay.uniform(low=1, high=max_delay))
        # if i == 0:
        #   d_value = 16.0
        # if i == 1:
        #   d_value = 17.0
        # if i == 2:
        #   d_value = 33.0
        delays.append(float(delay))
        singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, delay)
        connections.append(singleConnection)

    injectionConnection = [(0, 0, weight_to_spike, 1)]
    spikeArray = {'spike_times': [[0]]}

    populations.append(p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                                    label='pop_1'))

    populations.append(p.Population(1, p.SpikeSourceArray(**spikeArray),
                                    label='inputSpikes_1'))
    # populations[0].set_mapping_constraint({"x": 1, "y": 0})

    projections.append(p.Projection(populations[0], populations[0],
                                    p.FromListConnector(connections),
                                    p.StaticSynapse(weight=weight_to_spike,
                                                    delay=delay)))
    projections.append(p.Projection(populations[1], populations[0],
                                    p.FromListConnector(injectionConnection),
                                    p.StaticSynapse(weight=weight_to_spike,
                                                    delay=1)))

    p.external_devices.activate_live_output_for(populations[0])
    populations[0].set_constraint(ChipAndCoreConstraint(0, 0, 4))
    populations[1].set_constraint(ChipAndCoreConstraint(0, 0, 5))

    run_time = 100
    print("Running for {} ms".format(run_time))

    populations[0].record(['spikes'])
    p.run(run_time)

    # v = None
    # gsyn = None
    spikes = None
    spikes = neo_convertor.convert_spikes(populations[0].get_data(['spikes']))
    # print(projections[0].getWeights())
    # print(projections[0].getDelays())
    # print(delays)

    p.end()

    return spikes


class SynfireChainBB2pop_BStest(BaseTestCase):

    def test_synfire_chain_BB_2pop_ABS_test(self):
        spikes = do_run()
        self.assertEqual(20, len(spikes))
        spike_checker.synfire_spike_checker(spikes, nNeurons)


if __name__ == '__main__':
    import pylab

    spikes = do_run()
    if spikes is not None:
        print(spikes)
        pylab.figure()
        pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], ".")
        pylab.ylabel('neuron id')
        pylab.xlabel('Time/ms')
        pylab.yticks([0, 2, 4, 6, 8, 10])
        pylab.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        pylab.title('spikes')
        pylab.show()
    else:
        print("No spikes received")

    # Make some graphs
    """ticks = len(v) / nNeurons

    if v != None:
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('v')
        pylab.title('v')
        for pos in range(0, nNeurons, 20):
            v_for_neuron = v[pos * ticks : (pos + 1) * ticks]
            pylab.plot([i[1] for i in v_for_neuron],
                    [i[2] for i in v_for_neuron])
        pylab.show()

    if gsyn != None:
        pylab.figure()
        pylab.xlabel('Time/ms')
        pylab.ylabel('gsyn')
        pylab.title('gsyn')
        for pos in range(0, nNeurons, 20):
            gsyn_for_neuron = gsyn[pos * ticks : (pos + 1) * ticks]
            pylab.plot([i[1] for i in gsyn_for_neuron],
                    [i[2] for i in gsyn_for_neuron])
        pylab.show()
    """
