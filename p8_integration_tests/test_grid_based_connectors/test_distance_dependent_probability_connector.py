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

    def create_grid(n, label, dx=1.0, dy=1.0):
        grid_structure = p.Grid2D(dx=dx, dy=dy, x0=0.0, y0=0.0)
        return p.Population(n*n, p.IF_curr_exp(**cell_params_lif),
                            structure=grid_structure, label=label)

    # Parameters
    n = 10
    weight_to_spike = 5.0
    delay = 5
    runtime = 200

    # Network population
    grid = create_grid(n, 'grid')

    # SpikeInjector
    injectionConnection = [(0, n*n//2)]
    spikeArray = {'spike_times': [[5]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray),
                           label='inputSpikes_1')

    projections = list()

    # Projection for injector
    projections.append(
        p.Projection(inj_pop, grid, p.FromListConnector(injectionConnection),
                     p.StaticSynapse(weight=weight_to_spike, delay=delay)))

    # Simple connectors
    dist_dep_exc = "d<2.1"
    dist_dep_inh = "d<1.1"

    exc_connector = p.DistanceDependentProbabilityConnector(
        dist_dep_exc, allow_self_connections=True)
    inh_connector = p.DistanceDependentProbabilityConnector(
        dist_dep_inh, allow_self_connections=True)

    # Projections within grid
    projections.append(
        p.Projection(grid, grid, exc_connector,
                     p.StaticSynapse(weight=5.0, delay=10),
                     receptor_type='excitatory'))
    projections.append(
        p.Projection(grid, grid, inh_connector,
                     p.StaticSynapse(weight=2.0, delay=10),
                     receptor_type='inhibitory'))

    pre_weights = list()
    for projection in projections:
        pre_weights.append(projection.get('weight', 'list'))

    grid.record(['v', 'spikes'])
    inj_pop.record(['spikes'])
    p.run(runtime)

    v = grid.get_data('v')
    spikes = grid.get_data('spikes')
    stim_spikes = inj_pop.get_data('spikes')

    if plot:
        Figure(
            # raster plot of the stimulus spike times
            Panel(stim_spikes.segments[0].spiketrains,
                  yticks=True, markersize=1.5, xlim=(0, runtime), xticks=True),
            # raster plot of the presynaptic neurons' spike times
            Panel(spikes.segments[0].spiketrains,
                  yticks=True, markersize=0.2, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neurons
            Panel(v.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential (mV)",
                  data_labels=[grid.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            title="Simple grid distance-dependent prob connector",
            annotations="Simulated with {}".format(p.name())
        )
        plt.show()

    post_weights = list()
    for projection in projections:
        post_weights.append(projection.get('weight', 'list'))

    p.end()

    return v, spikes, pre_weights, post_weights


class DistanceDependentProbabilityConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes, pre_weights, post_weights = do_run(plot=False)
        # any checks go here
        spikes_test = neo_convertor.convert_spikes(spikes)
        self.assertEquals(4970, len(spikes_test))
        self.assertEquals(5.0, pre_weights[1][0][2])
        self.assertEquals(2.0, post_weights[-1][0][2])


if __name__ == '__main__':
    v, spikes, pre_weights, post_weights = do_run(plot=True)
    print(len(neo_convertor.convert_spikes(spikes)))
    print('pre_weights: ', pre_weights)
    print('post_weights: ', post_weights)
