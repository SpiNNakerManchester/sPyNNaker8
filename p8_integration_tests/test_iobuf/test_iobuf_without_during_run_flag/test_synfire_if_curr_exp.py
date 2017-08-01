"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
from spinn_front_end_common.utilities import globals_variables
import os

n_neurons = 200  # number of neurons in each population
runtime = 5000
neurons_per_core = n_neurons / 2
synfire_run = TestRun()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime], record=False, record_v=False,
                           record_gsyn_exc=False, record_gsyn_inh=False)

        prov_path = globals_variables.get_simulator()._provenance_file_path
        files = os.listdir(prov_path)
        found_iobuf = False

        for protential_iobuf_file in files:
            if ("iobuf" in protential_iobuf_file and
                    ".txt" in protential_iobuf_file):
                found_iobuf = True

        if not found_iobuf:
            raise Exception("failed to write iobuf")


if __name__ == '__main__':
    x = SynfireIfCurrExp()
    x.test_run()


