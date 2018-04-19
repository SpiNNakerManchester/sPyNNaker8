import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from spynnaker8.utilities import neo_convertor

import numpy


def do_run(plot):

    p.setup(timestep=1.0)

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

    # Parameters
    nNeurons = 200
    weight_to_spike = 2.0
    delay = 17
    runtime = 5000
    p.set_number_of_neurons_per_core(p.IF_curr_exp, nNeurons / 2)

    # Population
    pop = p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                       label='pop_1')

    # create loopConnections array using numpy linspaces
    loopConnections = numpy.array(
        [numpy.linspace(0, nNeurons-1, nNeurons),
         numpy.linspace(1, nNeurons, nNeurons)],
        numpy.uint32)
    # connect the final neuron to the first neuron
    loopConnections[1, nNeurons-1] = 0

    # SpikeInjector
    injectionConnection = numpy.array([[0], [0]], numpy.uint32)
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray),
                           label='inputSpikes_1')

    # Projection for injector
    p.Projection(inj_pop, pop, p.ArrayConnector(injectionConnection),
                 p.StaticSynapse(weight=weight_to_spike, delay=1))

    # Projection within population
    p.Projection(pop, pop, p.ArrayConnector(loopConnections),
                 p.StaticSynapse(weight=weight_to_spike, delay=delay))

    pop.record(['v', 'spikes'])
    p.run(runtime)

    v = pop.get_data('v')
    spikes = pop.get_data('spikes')

    if plot:
        Figure(
            # raster plot of the presynaptic neurons' spike times
            Panel(spikes.segments[0].spiketrains,
                  yticks=True, markersize=1.2, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neurons
            Panel(v.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential (mV)",
                  data_labels=[pop.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            title="Testing ArrayConnector",
            annotations="Simulated with {}".format(p.name())
        )
        plt.show()

    p.end()

    return v, spikes


class ArrayConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here
        spikes_test = neo_convertor.convert_spikes(spikes)
        self.assertEquals(263, len(spikes_test))


if __name__ == '__main__':
    v, spikes = do_run(plot=True)
