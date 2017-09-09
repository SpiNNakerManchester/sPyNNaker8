"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun

n_neurons = 200  # number of neurons in each population
runtimes = [5000]
neurons_per_core = n_neurons / 2
synfire_run = TestRun()


class SynfireIfCurrExp(BaseTestCase):

    # TODO How to check this worked
    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=runtimes, record=False, record_v=False,
                           record_gsyn_exc=False, record_gsyn_inh=False)


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=runtimes, record=False, record_v=False,
                       record_gsyn_exc=False, record_gsyn_inh=False)
