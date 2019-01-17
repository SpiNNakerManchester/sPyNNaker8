"""
Synfirechain-like example
"""
import os
import pickle
import unittest
from unittest import SkipTest

from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
from spynnaker8.utilities import neo_compare
from spinn_front_end_common.utilities.exceptions import ConfigurationException

synfire_run = SynfireRunner()

n_neurons = 20  # number of neurons in each population
current_file_path = os.path.dirname(os.path.abspath(__file__))
current_spike_file_path = os.path.join(current_file_path, "spikes.pickle")
current_v_file_path = os.path.join(current_file_path, "v.pickle")
current_gsyn_file_path = os.path.join(current_file_path, "gsyn.pickle")


class TestMallocKeyAllocatorWithSynfire(BaseTestCase):
    """
    tests the printing of print v given a simulation
    """

    def test_end_before_print(self):
        with self.assertRaises(ConfigurationException):
            synfire_run.do_run(n_neurons, max_delay=14, time_step=1,
                               neurons_per_core=1, delay=1.7, run_times=[50],
                               spike_path=current_spike_file_path,
                               gsyn_path_exc=current_gsyn_file_path,
                               v_path=current_v_file_path,
                               end_before_print=True)

    # This throws a WEIRD Exception.
    def test_script(self):
        """
        test that tests the printing of v from a pre determined recording
        :return:
        """
        synfire_run.do_run(n_neurons, max_delay=14, time_step=1,
                           neurons_per_core=1, delay=1.7, run_times=[50],
                           spike_path=current_spike_file_path,
                           gsyn_path_exc=current_gsyn_file_path,
                           v_path=current_v_file_path, end_before_print=False)

        spikes_read = synfire_run.get_output_pop_spikes_neo()
        v_read = synfire_run.get_output_pop_voltage_neo()
        gsyn_read = synfire_run.get_output_pop_gsyn_exc_neo()

        try:
            with open(current_spike_file_path, "r") as spike_file:
                spikes_saved = pickle.load(spike_file)
            with open(current_v_file_path, "r") as v_file:
                v_saved = pickle.load(v_file)
            with open(current_gsyn_file_path, "r") as gsyn_file:
                gsyn_saved = pickle.load(gsyn_file)

            neo_compare.compare_blocks(spikes_read, spikes_saved)
            neo_compare.compare_blocks(v_read, v_saved)
            neo_compare.compare_blocks(gsyn_read, gsyn_saved)
        except UnicodeDecodeError:
            raise SkipTest(
                "https://github.com/NeuralEnsemble/python-neo/issues/529")


if __name__ == '__main__':
    unittest.main()
