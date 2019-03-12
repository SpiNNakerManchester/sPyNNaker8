import os
from spinn_front_end_common.utilities import globals_variables
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestIobuffMultirun(BaseTestCase):

    def check_size(self, prov_path):
        iofile = os.path.join(
            prov_path, "iobuf_for_chip_0_0_processor_id_3.txt")
        return os.path.getsize(iofile)

    def test_run(self):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        prov_path = globals_variables.get_simulator()._provenance_file_path
        sim.Population(10, sim.IF_curr_exp(), label='pop_1')
        sim.run(500)
        size1 = self.check_size(prov_path)
        sim.run(500)
        size2 = self.check_size(prov_path)
        sim.run(500)
        size3 = self.check_size(prov_path)
        sim.reset()
        sim.run(500)
        size4 = self.check_size(prov_path)
        sim.run(500)
        size5 = self.check_size(prov_path)
        sim.reset()
        sim.Population(10, sim.IF_curr_exp(), label='pop_1')
        sim.run(500)
        prov_patha = globals_variables.get_simulator()._provenance_file_path
        size6 = self.check_size(prov_patha)
        sim.end()
        size7 = self.check_size(prov_patha)
        size8 = self.check_size(prov_patha)

        print(size1, size2, size3, size4, size5, size6, size7, size8)
