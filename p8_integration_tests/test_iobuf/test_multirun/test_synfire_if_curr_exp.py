"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

n_neurons = 200  # number of neurons in each population
runtimes = [1000, 1000, 1000, 1000, 1000]
neurons_per_core = n_neurons / 2
synfire_run = TestRun()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=runtimes, record=True, record_v=True,
                           record_gsyn=True)
        spikes = synfire_run.get_output_pop_spikes()

        self.assertEquals(53, len(spikes[0]))
        self.assertEquals(106, len(spikes[1]))
        self.assertEquals(158, len(spikes[2]))
        self.assertEquals(211, len(spikes[3]))
        self.assertEquals(263, len(spikes[4]))
        spike_checker.synfire_spike_checker(spikes, n_neurons)


if __name__ == '__main__':
    results = synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                                 run_times=runtimes, record=True,
                                 record_v=True, record_gsyn=True)
    gsyn = synfire_run.get_output_pop_gsyn()
    v = synfire_run.get_output_pop_voltage()
    spikes = synfire_run.get_output_pop_spikes()
    print len(spikes[0]), len(spikes[1]), len(spikes[2]), len(spikes[3]), \
        len(spikes[4])

    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
