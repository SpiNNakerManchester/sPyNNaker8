import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from spynnaker8.utilities import neo_convertor


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
    n = 6
    weight_to_spike = 3.0
    delay = 2
    runtime = 200

    # Network population
    pop_1 = p.Population(n, p.IF_curr_exp(**cell_params_lif), label='pop_1')
    pop_2 = p.Population(n/2, p.IF_curr_exp(**cell_params_lif), label='pop_2')

    # SpikeInjector
    injectionConnection = [(0, n/2)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray),
                           label='inputSpikes_1')

    # Projection for injector
    p.Projection(inj_pop, pop_1, p.FromListConnector(injectionConnection),
                 p.StaticSynapse(weight=weight_to_spike, delay=delay))

    # Simple connectors
    index_based_exc = "(i+j)/"+str(n*(n-n/2.0))
    index_based_exc2 = "2.0*(i+j)/"+str(n*(n-n/2.0))
    index_based_inh = "(i+j)/"+str(n*(n+n/2.0))
    print 'index_based_exc: ', index_based_exc
    print 'index_based_inh: ', index_based_inh

    exc_connector = p.IndexBasedProbabilityConnector(
        index_based_exc, allow_self_connections=True)
    inh_connector = p.IndexBasedProbabilityConnector(
        index_based_inh, allow_self_connections=False)
    exc_connector2 = p.IndexBasedProbabilityConnector(
        index_based_exc2, allow_self_connections=True)

    # Projections within grid
    p.Projection(pop_1, pop_1, exc_connector,
                 p.StaticSynapse(weight=2.0, delay=5))
    p.Projection(pop_1, pop_1, inh_connector,
                 p.StaticSynapse(weight=1.5, delay=5))

    p.Projection(pop_1, pop_2, exc_connector2,
                 p.StaticSynapse(weight=1.5, delay=2))

    pop_1.record(['v', 'spikes'])
    pop_2.record(['v', 'spikes'])

    p.run(runtime)

    v = pop_1.get_data('v')
    spikes = pop_1.get_data('spikes')
    v2 = pop_2.get_data('v')
    spikes2 = pop_2.get_data('spikes')

    if plot:
        Figure(
            # raster plot of the presynaptic neurons' spike times
            Panel(spikes.segments[0].spiketrains,
                  yticks=True, markersize=2.0, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neurons
            Panel(v.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential pop 1 (mV)",
                  data_labels=[pop_1.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            # raster plot of the presynaptic neurons' spike times
            Panel(spikes2.segments[0].spiketrains,
                  yticks=True, markersize=2.0, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neurons
            Panel(v2.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential pop 2 (mV)",
                  data_labels=[pop_2.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            title="Simple grid distance-dependent probability connector",
            annotations="Simulated with {}".format(p.name())
        )
        plt.show()

    p.end()

    return v, spikes, v2, spikes2


class DistanceDependentProbabilityConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes, v2, spikes2 = do_run(plot=False)
        # any checks go here
        spikes_test = neo_convertor.convert_spikes(spikes)
        spikes_test2 = neo_convertor.convert_spikes(spikes2)
        self.assertGreater(len(spikes_test), len(spikes_test2))


if __name__ == '__main__':
    v, spikes, v2, spikes2 = do_run(plot=True)
