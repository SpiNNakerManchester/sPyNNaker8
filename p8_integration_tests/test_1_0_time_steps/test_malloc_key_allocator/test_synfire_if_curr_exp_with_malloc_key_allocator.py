"""
Synfirechain-like example
"""
import unittest
import os
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
import spynnaker.pyNN.utilities.utility_calls as utility_calls
from spinn_front_end_common.utilities.exceptions import ConfigurationException

synfire_run = TestRun()

n_neurons = 20  # number of neurons in each population
current_file_path = os.path.dirname(os.path.abspath(__file__))
current_spike_file_path = os.path.join(current_file_path, "spikes.data")
current_v_file_path = os.path.join(current_file_path, "v.data")
current_gsyn_file_path = os.path.join(current_file_path, "gsyn.data")


class TestMallocKeyAllocatorWithSynfire(BaseTestCase):
    """
    tests the printing of print v given a simulation
    """

    def test_end_before_print(self):
        with self.assertRaises(ConfigurationException):
            synfire_run.do_run(n_neurons, max_delay=14, time_step=1,
                               neurons_per_core=1, delay=1.7, run_times=[50],
                               spike_path=current_spike_file_path,
                               gsyn_path=current_gsyn_file_path,
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
                           gsyn_path=current_gsyn_file_path,
                           v_path=current_v_file_path, end_before_print=False)
        gsyn = synfire_run.get_output_pop_gsyn()
        v = synfire_run.get_output_pop_voltage()
        spikes = synfire_run.get_output_pop_spikes()

        read_in_spikes = utility_calls.read_spikes_from_file(
            current_spike_file_path, 0, n_neurons, 0, 5000)
        read_in_v = utility_calls.read_in_data_from_file(
            current_v_file_path, 0, n_neurons, 0, 5000)
        read_in_gsyn = utility_calls.read_in_data_from_file(
            current_gsyn_file_path, 0, n_neurons, 0, 5000)

        for spike_element, read_element in zip(spikes, read_in_spikes):
            self.assertEqual(round(spike_element[0], 1),
                             round(read_element[0], 1))
            self.assertEqual(round(spike_element[1], 1),
                             round(read_element[1], 1))

        for v_element, read_element in zip(v, read_in_v):
            self.assertEqual(round(v_element[0], 1),
                             round(read_element[0], 1))
            self.assertEqual(round(v_element[1], 1),
                             round(read_element[1], 1))

        for gsyn_element, read_element in zip(gsyn, read_in_gsyn):
            self.assertEqual(round(gsyn_element[0], 1),
                             round(read_element[0], 1))
            self.assertEqual(round(gsyn_element[1], 1),
                             round(read_element[1], 1))


if __name__ == '__main__':
    unittest.main()
