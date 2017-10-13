import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


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

    def create_grid(n, label, dx=1.0, dy=1.0):
        grid_structure = p.Grid2D(dx=dx, dy=dy, x0=0.0, y0=0.0)
        return p.Population(n*n, p.IF_curr_exp(**cell_params_lif),
                            structure=grid_structure, label=label)


    # Parameters
    n = 5
    weight_to_spike = 5.0
    delay = 2
    runtime=1000

    # Network population
    small_world = create_grid(n, 'small_world')

    # SpikeInjector
    injectionConnection = [(0, 0)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray), label='inputSpikes_1')
    p.Projection(inj_pop, small_world, p.FromListConnector(injectionConnection),
                 p.StaticSynapse(weight=weight_to_spike, delay=delay))

    # Connectors
    degree = 2
    rewiring = 0.4
    small_world_connector = p.SmallWorldConnector(degree, rewiring)

    # Projection for small world grid
    p.Projection(small_world, small_world, small_world_connector,
                 p.StaticSynapse(weight=2.0, delay=5))

    small_world.record(['v','spikes'])

    p.run(runtime)

    v = small_world.get_data('v')
    spikes = small_world.get_data('spikes')

    if plot:
        Figure(
            # raster plot of the presynaptic neuron spike times
            Panel(spikes.segments[0].spiketrains,
                  yticks=True, markersize=0.2, xlim=(0, runtime), xticks=True),
            # membrane potential of the postsynaptic neuron
            Panel(v.segments[0].filter(name='v')[0],
                  ylabel="Membrane potential (mV)",
                  data_labels=[small_world.label], yticks=True,
                  xlim=(0, runtime), xticks=True),
            title="Simple small world connector",
            annotations="Simulated with {}".format(p.name())
        )
        plt.show()

    p.end()

    return v, spikes


class SmallWorldConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here

if __name__ == '__main__':
    v, spikes = do_run(plot=True)
