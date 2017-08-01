"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from spinn_front_end_common.utilities import globals_variables
import os
import spynnaker8 as p


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        p.Population(10, p.IF_curr_exp(), label='pop_1')
        p.run(500)

        prov_path = globals_variables.get_simulator()._provenance_file_path
        p.end()

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
