"""
Synfirechain-like example
"""
from testfixtures import LogCapture
from unittest import SkipTest

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
        raise SkipTest("Broken in master but to be fixed in new SDRAm branch")

        with LogCapture() as lc:
            synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                               run_times=[runtime])
            spikes = synfire_run.get_output_pop_spikes_numpy()
            # CB Currently three but could change needs to be > 1
            # Needs to be less than test_shorter_run_version
            self.assert_logs_messages(
                lc.records, "*** Running simulation... ***", 'INFO', 3)

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
