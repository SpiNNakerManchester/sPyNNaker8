import p8_integration_tests.scripts.pynnBrunnelPlot as pblt

from p8_integration_tests.base_test_case import BaseTestCase
import p8_integration_tests.scripts.pynnBrunnelBrianNestSpinnaker as script
from spynnaker8.utilities import neo_convertor
from unittest import SkipTest

Neurons = 3000  # number of neurons in each population
sim_time = 1000
simulator_Name = 'spiNNaker'


def plot(esp, sim_time, N_E):
    import pylab  # deferred so unittest are not dependent on it
    if esp is not None:
        ts_ext = [x[1] for x in esp]
        ids_ext = [x[0] for x in esp]
        title = 'Raster Plot of the excitatory population in %s' \
                % simulator_Name,
        pblt._make_plot(ts_ext, ts_ext, ids_ext, ids_ext,
                        len(ts_ext) > 0, 5.0, False, title,
                        'Simulation Time (ms)', total_time=sim_time,
                        n_neurons=N_E)

        pylab.show()


class PynnBrunnelBrianNestSpinnaker(BaseTestCase):

    # AttributeError: 'SpikeSourcePoisson' object has no attribute 'describe'
    def test_run(self):
        self.assert_not_spin_three()
        (esp, s, N_E) = script.do_run(
            Neurons, sim_time, record=True, seed=1)
        esp_numpy = neo_convertor.convert_spikes(esp)
        s_numpy = neo_convertor.convert_spikes(s)
        self.assertEquals(2400, N_E)
        self.assertEquals(224, len(esp_numpy))
        self.assertEquals(23896, len(s_numpy))


if __name__ == '__main__':
    (esp, s, N_E) = script.do_run(Neurons, sim_time, record=True, seed=1)
    esp_numpy = neo_convertor.convert_spikes(esp)
    s_numpy = neo_convertor.convert_spikes(s)
    plot(esp_numpy, sim_time, N_E)
    print(len(esp_numpy))
    print(len(s_numpy))
    print(N_E)
