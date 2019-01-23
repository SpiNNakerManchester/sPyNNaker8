import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from spynnaker8.utilities import neo_convertor

import os
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
                       'v_thresh': -40.0
                       }

    # Parameters
    n = 10
    weight_to_spike = 5.0
    delay = 5
    runtime = 200

    # Populations
    exc_pop = p.Population(n, p.IF_curr_exp(**cell_params_lif),
                           label='exc_pop')
    inh_pop = p.Population(n, p.IF_curr_exp(**cell_params_lif),
                           label='inh_pop')

    # SpikeInjector
    injectionConnection = [(0, 0)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray),
                           label='inputSpikes_1')

    # Projection for injector
    p.Projection(inj_pop, exc_pop, p.FromListConnector(injectionConnection),
                 p.StaticSynapse(weight=weight_to_spike, delay=delay))

    # Set up fromfileconnectors by writing to file
    connection_list1 = [
                (0, 0, 0.1, 10),
                (3, 0, 0.2, 11),
                (2, 3, 0.3, 12),
                (5, 1, 0.4, 13),
                (0, 1, 0.5, 14),
                ]
    path1 = "test1.connections"
    if os.path.exists(path1):
        os.remove(path1)

    current_file_path = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(current_file_path, path1)
    numpy.savetxt(file1, connection_list1)
    file_connector1 = p.FromFileConnector(file1)

    # PyNN allows the column order (after i,j) to be different,
    # so we can test that here
    connection_list2 = [
                (4, 9, 12, 0.3),
                (1, 5, 13, 0.4),
                (7, 6, 1, 0.1),
                (6, 5, 14, 0.5),
                (8, 2, 11, 0.2),
                ]
    path2 = "test2.connections"
    if os.path.exists(path2):
        os.remove(path2)

    file2 = path2
    numpy.savetxt(file2, connection_list2,
                  header='columns = ["i", "j", "delay", "weight"]')
    file_connector2 = p.FromFileConnector(file2)

    # Projections within populations
    p.Projection(exc_pop, inh_pop, file_connector1,
                 p.StaticSynapse(weight=2.0, delay=5))
    p.Projection(inh_pop, exc_pop, file_connector2,
                 p.StaticSynapse(weight=1.5, delay=10))

    exc_pop.record(['v', 'spikes'])
    inh_pop.record(['v', 'spikes'])
    p.run(runtime)

    v_exc = exc_pop.get_data('v')
    spikes_exc = exc_pop.get_data('spikes')

    if plot:
        Figure(
            # raster plot of the presynaptic neurons' spike times
            Panel(spikes_exc.segments[0].spiketrains,
                  yticks=True, markersize=1.2, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neurons
            Panel(v_exc.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential (mV)",
                  data_labels=[exc_pop.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            title="Testing FromFileConnector",
            annotations="Simulated with {}".format(p.name())
        )
        plt.show()

    p.end()

    return v_exc, spikes_exc


class FromFileConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here
        spikes_test = neo_convertor.convert_spikes(spikes)
        self.assertEquals(2, len(spikes_test))


if __name__ == '__main__':
    v, spikes = do_run(plot=True)
