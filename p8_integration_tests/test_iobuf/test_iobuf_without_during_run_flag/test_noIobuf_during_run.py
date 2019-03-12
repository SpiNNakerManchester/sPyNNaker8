"""
Synfirechain-like example
"""
import os
from spinn_front_end_common.utilities import globals_variables
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoIobufDuringRun(BaseTestCase):

    def check_for_oibufs(self):
        prov_path = globals_variables.get_simulator()._provenance_file_path

        files = os.listdir(prov_path)

        for protential_iobuf_file in files:
            if ("iobuf" in protential_iobuf_file and
                    ".txt" in protential_iobuf_file):
                return True
        return False

    def test_run(self):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        sim.Population(10, sim.IF_curr_exp(), label='pop_1')
        sim.run(500)

        self.assertFalse(self.check_for_oibufs())
        sim.end()
        self.assertFalse(self.check_for_oibufs())


if __name__ == '__main__':
    x = TestNoIobufDuringRun()
    x.test_run()
