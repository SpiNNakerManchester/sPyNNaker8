"""
Synfirechain-like example
"""
# general imports
import os
import pickle
import unittest
from unittest import SkipTest
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
from spinnman.exceptions import SpinnmanTimeoutException
from spynnaker8.utilities import neo_compare

n_neurons = 200  # number of neurons in each population
runtime = 500
current_file_path = os.path.dirname(os.path.abspath(__file__))
current_v_file_path = os.path.join(current_file_path, "v.pickle")
max_delay = 14
timestep = 0.1
neurons_per_core = n_neurons/2
delay = 1.7
synfire_run = SynfireRunner()


class TestPrintVoltage(BaseTestCase):
    """
    tests the printing of print v given a simulation
    """

    def test_print_voltage(self):
        """
        test that tests the printing of v from a pre determined recording
        :return:
        """
        try:
            synfire_run.do_run(n_neurons, max_delay=max_delay,
                               time_step=timestep,
                               neurons_per_core=neurons_per_core, delay=delay,
                               run_times=[runtime], v_path=current_v_file_path)
            v_read = synfire_run.get_output_pop_voltage_neo()

            try:
                with open(current_v_file_path, "r") as v_file:
                    v_saved = pickle.load(v_file)
                neo_compare.compare_blocks(v_read, v_saved)
            except UnicodeDecodeError:
                raise SkipTest(
                    "https://github.com/NeuralEnsemble/python-neo/issues/529")
            finally:
                os.remove(current_v_file_path)
            # System intentional overload so may error
        except SpinnmanTimeoutException as ex:
            raise SkipTest(ex)


if __name__ == '__main__':
    unittest.main()
