import numpy
import spynnaker.plot_utils as plot_utils
import spynnaker8 as p
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def do_run(n_neurons, n_cores, i_offset2, i_offset3):
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

    populations[0].record("spikes")

    p.run(100)

    populations[0].set(i_offset=i_offset2)

    p.run(100)

    populations[0].set(i_offset=i_offset3)

    p.run(100)

    neo = populations[0].get_data()

    p.end()

    return neo


class TestSetTOffset(BaseTestCase):
    expected = [104., 112., 120., 128., 136., 144., 152., 160., 168., 176.,
                184., 192., 200., 205., 210., 215., 220., 225., 230., 235.,
                240., 245., 250., 255., 260., 265., 270., 275., 280., 285.,
                290., 295.]

    def test_one_core(self):
        n_neurons = 6
        n_cores = 1
        neo = do_run(n_neurons, n_cores, 1, 2)
        spiketrains = neo.segments[0].spiketrains
        for spiketrain in spiketrains:
            assert numpy.array_equal(spiketrain.magnitude, self.expected)

    def test_three_cores(self):
        n_neurons = 6
        n_cores = 3
        neo = do_run(n_neurons, n_cores, 1, 2)
        spiketrains = neo.segments[0].spiketrains
        try:
            for spiketrain in spiketrains:
                assert numpy.array_equal(spiketrain.magnitude, self.expected)
        except AssertionError:
            self.known_issue(
                "https://github.com/SpiNNakerManchester/sPyNNaker/issues/603")


if __name__ == '__main__':
    n_neurons = 40
    n_cores = 3
    neo = do_run(n_neurons, n_cores, 1, 2)
    spikes = neo_convertor.convert_spikes(neo)
    v = neo_convertor.convert_data(neo, "v")
    gsyn = neo_convertor.convert_data(neo, "gsyn_exc")

    print(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)

    times = set(spikes[:, 1])
    print(n_neurons * len(times), len(spikes))
