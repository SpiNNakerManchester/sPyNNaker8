"""
Synfirechain-like example
"""
import spynnaker8 as p
import spynnaker.plot_utils as plot_utils
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(n_neurons, n_cores, new_i_offset):
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    p.set_number_of_neurons_per_core("IF_curr_exp", n_neurons / n_cores)

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

    populations[0].record_v()
    populations[0].record_gsyn()
    populations[0].record()

    p.run(2000)

    populations[0].set('i_offset', new_i_offset)

    p.run(2000)

    spikes = populations[0].getSpikes(compatible_output=True)
    v = populations[0].get_v(compatible_output=True)
    gsyn = populations[0].get_gsyn(compatible_output=True)

    p.end()

    return (spikes, v, gsyn)


def check_spikes(n_neurons, spikes):
    times = set(spikes[:, 1])
    print n_neurons * len(times), len(spikes)


class TestSetTOffset(BaseTestCase):

    def test_one_core(self):
        n_neurons = 40
        n_cores = 1
        (spikes, v, gsyn) = do_run(n_neurons, n_cores, 0.1875)
        times = set(spikes[:, 1])
        self.assertEquals(n_neurons * len(times), len(spikes))

    def test_three_cores(self):
        n_neurons = 40
        n_cores = 3
        (spikes, v, gsyn) = do_run(n_neurons, n_cores, 0.1875)
        times = set(spikes[:, 1])
        self.assertEquals(n_neurons * len(times), len(spikes))


if __name__ == '__main__':
    n_neurons = 40
    n_cores = 3
    (spikes, v, gsyn) = do_run(n_neurons, 3, 0.1875)

    print spikes
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)

    times = set(spikes[:, 1])
    print n_neurons * len(times), len(spikes)
