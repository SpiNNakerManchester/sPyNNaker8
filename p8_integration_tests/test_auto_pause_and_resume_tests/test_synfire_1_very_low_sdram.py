"""
Synfirechain-like example
"""
from testfixtures import LogCapture

from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

n_neurons = 200  # number of neurons in each population
runtime = 3000
neurons_per_core = n_neurons / 2
synfire_run = SynfireRunner()


class TestVeryLow(BaseTestCase):
    """
    tests the run is split by auto pause resume
    """

    def test_get_multi_run(self):
        # CB Jan 22 2019  Currrently not doing auto pause
        #with LogCapture() as lc:
            # CB Jan 14 2019 Current version splits over too many chips.
        self.assert_not_spin_three()
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime])
        spikes = synfire_run.get_output_pop_spikes_numpy()
            # self.assert_logs_messages(
            #    lc.records, "*** Running simulation... ***", 'INFO', 2,
            #    allow_more=True)

        self.assertEquals(158, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        synfire_run.get_output_pop_gsyn_exc_numpy()
        synfire_run.get_output_pop_voltage_numpy()


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=[runtime])
    gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_numpy()

    print(len(spikes))
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
