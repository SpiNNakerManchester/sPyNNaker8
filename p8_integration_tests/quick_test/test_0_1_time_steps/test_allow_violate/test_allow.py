# general imports
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.spike_checker as spike_checker
from spinnman.exceptions import SpinnmanTimeoutException
from unittest import SkipTest

n_neurons = 10  # number of neurons in each population
runtime = 50
synfire_run = SynfireRunner()


class TestAllow(BaseTestCase):
    """
    Tests the running of a silumation at faster than real time.
    Success criteria.
        1. Run without errors
        2. Synfire like spike pattern
    """

    def test_allow(self):
        try:
            synfire_run.do_run(
                n_neurons, max_delay=14.4, time_step=0.1,
                neurons_per_core=5, delay=1.7, run_times=[runtime])

            spikes = synfire_run.get_output_pop_spikes_numpy()
            # no check of spikes length as the system overloads
            spike_checker.synfire_spike_checker(spikes, n_neurons)
            # no check of gsyn as the system overloads
        # System intentional overload so may error
        except SpinnmanTimeoutException as ex:
            raise SkipTest(ex)
