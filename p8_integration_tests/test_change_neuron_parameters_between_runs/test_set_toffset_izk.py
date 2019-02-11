"""
Synfirechain-like example
"""
import spynnaker.plot_utils as plot_utils
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(n_neurons, n_cores, new_i_offset):
    p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
    p.set_number_of_neurons_per_core(p.Izhikevich, n_neurons / n_cores)

    cell_params_izk = {'a': 0.02,
                       'b': 0.2,
                       'c': -65,
                       'd': 8,
                       'v': -75,
                       'u': 0,
                       'tau_syn_E': 2,
                       'tau_syn_I': 2,
                       'i_offset': 0
                       }

    populations = list()

    populations.append(p.Population(n_neurons, p.Izhikevich, cell_params_izk,
                                    label='pop_1'))

    populations[0].record("all")

    p.run(2000)

    populations[0].set(i_offset=new_i_offset)

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
        for spiketrain in spiketrains:
            self.assertEquals(0,  len(spiketrain))

    def test_three_cores(self):
        n_neurons = 40
        n_cores = 3
        neo = do_run(n_neurons, n_cores, 0.1875)
        spiketrains = neo.segments[0].spiketrains
        for spiketrain in spiketrains:
            self.assertEquals(0,  len(spiketrain))


if __name__ == '__main__':
    n_neurons = 40
    n_cores = 3
    neo = do_run(n_neurons, n_cores, 0.1875)
    spikes = neo_convertor.convert_spikes(neo)
    v = neo_convertor.convert_data(neo, "v")
    gsyn = neo_convertor.convert_data(neo, "gsyn_exc")

    print(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)

    times = set(spikes[:, 1])
    print(n_neurons * len(times), len(spikes))
