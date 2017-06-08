"""
Synfirechain-like example
"""
import spynnaker8 as p
import spynnaker.plot_utils as plot_utils
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(n_neurons, n_cores, new_i_offset):
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    p.set_number_of_neurons_per_core(p.IF_curr_exp, n_neurons / n_cores)

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

    populations.append(p.Population(n_neurons, p.IF_curr_exp, cell_params_lif,
                                    label='pop_1'))

    populations[0].record("all")

    p.run(2000)

    populations[0].set('i_offset', new_i_offset)

    p.run(2000)

    neo = populations[0].get_data()

    p.end()

    return neo


class TestSetTOffset(BaseTestCase):

    def test_one_core(self):
        n_neurons = 40
        n_cores = 1
        neo = do_run(n_neurons, n_cores, 0.1875)
        spiketrains = neo.segments[0].spiketrains
        length = len(spiketrains)
        for spiketrain in spiketrains:
            self.assertEquals(length,  len(spiketrain))

    def test_three_cores(self):
        n_neurons = 40
        n_cores = 3
        neo = do_run(n_neurons, n_cores, 0.1875)
        spiketrains = neo.segments[0].spiketrains
        length = len(spiketrains)
        for spiketrain in spiketrains:
            self.assertEquals(length,  len(spiketrain))


if __name__ == '__main__':
    n_neurons = 40
    n_cores = 3
    neo = do_run(n_neurons, n_cores, 0.1875)
    spikes = neo_convertor.convert_spikes(neo)
    v = neo_convertor.convert_data(neo, "v")
    gsyn = neo_convertor.convert_data(neo, "gsyn_exc")

    print spikes
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)

    times = set(spikes[:, 1])
    print n_neurons * len(times), len(spikes)
