"""
Synfirechain-like example
"""
import os
import pickle
import unittest
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
from spynnaker8.utilities import neo_compare

from spinnman.exceptions import SpinnmanTimeoutException
from unittest import SkipTest

n_neurons = 20
timestep = 0.1
max_delay = 14.40
delay = 1.7
neurons_per_core = n_neurons/2
runtime = 500
current_file_path = os.path.dirname(os.path.abspath(__file__))
spike_path = os.path.join(current_file_path, "spikes.pickle")
synfire_run = TestRun()


class TestPrintSpikes(BaseTestCase):
    """
    tests the printing of get spikes given a simulation
    """

    def test_print_spikes(self):
        try:
            synfire_run.do_run(n_neurons, time_step=timestep,
                               max_delay=max_delay, delay=delay,
                               neurons_per_core=neurons_per_core,
                               run_times=[runtime],
                               spike_path=spike_path)
            spikes = synfire_run.get_output_pop_spikes_neo()

            with open(spike_path, "r") as spike_file:
                read_in_spikes = pickle.load(spike_file)

            neo_compare.compare_blocks(spikes, read_in_spikes)

        except SpinnmanTimeoutException as ex:
            # System intentional overload so may error
            raise SkipTest(ex)


if __name__ == '__main__':
    unittest.main()
