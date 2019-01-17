import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
import pylab
import csa


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

    n = 13  # 10  # 5
    p.set_number_of_neurons_per_core(p.IF_curr_exp, n)
    weight_to_spike = 2.0
    delay = 5
    runtime = 200

    # Network
    grid = csa.grid2d(n, xScale=1.0*n, yScale=1.0*n)

    # SpikeInjector
    injectionConnection = [(0, 0)]
    spikeArray = {'spike_times': [[0]]}
    inj_pop = p.Population(1, p.SpikeSourceArray(**spikeArray),
                           label='inputSpikes_1')

    # grid population
    grid_pop = p.Population(n*n, p.IF_curr_exp(**cell_params_lif),
                            label='grid_pop')

    p.Projection(inj_pop, grid_pop, p.FromListConnector(injectionConnection),
                 p.StaticSynapse(weight=weight_to_spike, delay=delay))

    # Connectors
    exc_connector_set = csa.disc(2.5)*csa.euclidMetric2d(grid)
    exc_connector = p.CSAConnector(exc_connector_set)

    inh_connector_set = csa.disc(1.5)*csa.euclidMetric2d(grid)
    inh_connector = p.CSAConnector(inh_connector_set)

    # Wire grid
    p.Projection(grid_pop, grid_pop, exc_connector,
                 p.StaticSynapse(weight=2.0, delay=10))
    p.Projection(grid_pop, grid_pop, inh_connector,
                 p.StaticSynapse(weight=0.5, delay=15))

    grid_pop.record(['v', 'spikes'])

    p.run(runtime)

    v = grid_pop.spinnaker_get_data('v')
    spikes = grid_pop.spinnaker_get_data('spikes')

    if plot:
        # original grid
        csa.gplot2d(grid, n*n)

        # excitatory connector
        exc_connector.show_connection_set()
        csa.gplotsel2d(grid, exc_connector_set, range(n*n), range(n*n), N0=n*n)

        # inhibitory connector
        inh_connector.show_connection_set()
        csa.gplotsel2d(grid, inh_connector_set, range(n*n), range(n*n), N0=n*n)

        # Now plot spikes and v
        pylab.figure()
        pylab.plot([i[1] for i in spikes],
                   [i[0] for i in spikes], "r.")
        pylab.xlabel('Time/ms')
        pylab.ylabel('spikes')
        pylab.title('spikes')

        pylab.show()

        pylab.figure()
        ticks = len(v) // (n*n)
        for pos in range(0, n*n):
            v_for_neuron = v[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[2] for i in v_for_neuron])
        pylab.xlabel('Time/ms')
        pylab.ylabel('V')
        pylab.title('membrane voltages per neuron')

        pylab.show()

    p.end()

    return v, spikes


class CSAGridConnectorTest(BaseTestCase):
    def test_run(self):
        v, spikes = do_run(plot=False)
        # any checks go here
        self.assertLess(7220, len(spikes))
        self.assertGreater(7225, len(spikes))
        self.assertEquals(33800, len(v))


if __name__ == '__main__':
    v, spikes = do_run(plot=True)
