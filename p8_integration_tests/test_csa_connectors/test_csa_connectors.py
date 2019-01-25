import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import pylab
import csa
import random
from unittest import SkipTest


def do_run(plot):
    random.seed(1)

    runtime = 3000
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    nNeurons = 200  # number of neurons in each population
    p.set_number_of_neurons_per_core(p.IF_curr_exp, nNeurons / 10)

    cell_params_lif = {'cm': 0.25,
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
    delay = 10

    # connection list in a loop for first population
    loopConnections = []
    for i in range(0, nNeurons):
        singleConnection = ((i, (i + 1) % nNeurons))
        loopConnections.append(singleConnection)

    # injection list to set the chain going
    injectionConnection = [(0, 0)]
    spikeArray = {'spike_times': [[0]]}

    # list of populations
    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_1'))
    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_2'))
    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_3'))
    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_4'))
    populations.append(
        p.Population(1, p.SpikeSourceArray(**spikeArray),
                     label='inputSpikes_1'))

    # Loop connector: we can just pass in the list we made earlier
    CSA_loop_connector = p.CSAConnector(loopConnections)

    # random connector: each connection has a probability of 0.05
    CSA_random_connector = p.CSAConnector(csa.random(0.05))

    # one-to-one connector: do I really need to explain?
    CSA_onetoone_connector = p.CSAConnector(csa.oneToOne)

    # This creates a block of size (5,10) with a probability of 0.05; then
    # within the block an individual connection has a probability of 0.3
    csa_block_random = csa.block(15, 10)*csa.random(0.05)*csa.random(0.3)
    CSA_randomblock_connector = p.CSAConnector(csa_block_random)

    # list of projections using the connectors above
    projections.append(p.Projection(
        populations[0], populations[0], CSA_loop_connector,
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))
    projections.append(p.Projection(
        populations[0], populations[1], CSA_random_connector,
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))
    projections.append(p.Projection(
        populations[1], populations[2], CSA_onetoone_connector,
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))
    projections.append(p.Projection(
        populations[2], populations[3], CSA_randomblock_connector,
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))
    projections.append(p.Projection(
        populations[4], populations[0],
        p.FromListConnector(injectionConnection),
        p.StaticSynapse(weight=weight_to_spike, delay=1)))

    populations[0].record(['v', 'spikes'])
    populations[1].record(['v', 'spikes'])
    populations[2].record(['v', 'spikes'])
    populations[3].record(['v', 'spikes'])

    p.run(runtime)

    # get data (could be done as one, but can be done bit by bit as well)
    v = populations[0].spinnaker_get_data('v')
    v2 = populations[1].spinnaker_get_data('v')
    v3 = populations[2].spinnaker_get_data('v')
    v4 = populations[3].spinnaker_get_data('v')
    spikes = populations[0].spinnaker_get_data('spikes')
    spikes2 = populations[1].spinnaker_get_data('spikes')
    spikes3 = populations[2].spinnaker_get_data('spikes')
    spikes4 = populations[3].spinnaker_get_data('spikes')

    if plot:
        # Use the show functionality of CSA to display connection sets
        CSA_loop_connector.show_connection_set()
        CSA_random_connector.show_connection_set()
        CSA_onetoone_connector.show_connection_set()
        CSA_randomblock_connector.show_connection_set()

        # Now plot some spikes
        pylab.figure()
        pylab.plot([i[1] for i in spikes],
                   [i[0] for i in spikes], "r.")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes: population 1')

        pylab.show()

        pylab.figure()
        pylab.plot([i[1] for i in spikes3],
                   [i[0] for i in spikes3], "g.")
        pylab.plot([i[1] for i in spikes4],
                   [i[0] for i in spikes4], "r.")
        pylab.plot([i[1] for i in spikes2],
                   [i[0] for i in spikes2], "b.")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes: populations 2, 3, 4')

        pylab.show()

    p.end()

    return v, v2, v3, v4, spikes, spikes2, spikes3, spikes4


class CSAConnectorTest(BaseTestCase):
    def test_run(self):
        try:
            v, v2, v3, v4, spikes, spikes2, spikes3, spikes4 = do_run(
                plot=False)
            # any checks go here
            self.assertEquals(250, len(spikes))
            self.assertEquals(2633, len(spikes2))
            self.assertEquals(2627, len(spikes3))
            self.assertEquals(10749, len(spikes4))
        except TypeError:
            raise SkipTest("https://github.com/INCF/csa/issues/10")


if __name__ == '__main__':
    v, v2, v3, v4, spikes, spikes2, spikes3, spikes4 = do_run(plot=True)
    print(len(spikes), len(spikes2), len(spikes3), len(spikes4))
