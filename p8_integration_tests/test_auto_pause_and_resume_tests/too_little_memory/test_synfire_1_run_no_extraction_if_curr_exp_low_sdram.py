"""
Synfirechain-like example
"""
import pytest

from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
from pacman.exceptions import PacmanPartitionException

n_neurons = 200  # number of neurons in each population
runtime = 3000
neurons_per_core = n_neurons / 2
synfire_run = SynfireRunner()


class TestGsyn(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """

    def test_get_gsyn(self):
        with pytest.raises(PacmanPartitionException):
            synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                               run_times=[runtime])


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=[runtime])
