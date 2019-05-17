import os
from spinn_front_end_common.utilities import globals_variables
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestIobuffMultirun(BaseTestCase):

    def check_size(self, prov_path):
        iofile = os.path.join(
            prov_path, "iobuf_for_chip_0_0_processor_id_3.txt")
        return os.path.getsize(iofile)

    def do_run(self):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        prov_path = globals_variables.get_simulator()._provenance_file_path
        sim.Population(10, sim.IF_curr_exp(), label='pop_1')
        sim.run(50)
        size1 = self.check_size(prov_path)
        sim.run(50)
        size2 = self.check_size(prov_path)
        self.assertGreater(size2, size1)
        sim.run(50)
        size3 = self.check_size(prov_path)
        self.assertGreater(size3, size2)

        # Soft reset so same provenance
        sim.reset()
        sim.run(50)
        size4 = self.check_size(prov_path)
        self.assertGreater(size4, size3)
        sim.run(50)
        size5 = self.check_size(prov_path)
        self.assertGreater(size5, size4)

        # hard reset so new provenance
        sim.reset()
        sim.Population(10, sim.IF_curr_exp(), label='pop_1')
        sim.run(50)
        prov_patha = globals_variables.get_simulator()._provenance_file_path
        self.assertNotEqual(prov_path, prov_patha)
        size6 = self.check_size(prov_patha)
        # Should write the same thing again
        self.assertEquals(size1, size6)
        sim.end()

        # Should not add anything on end.
        size7 = self.check_size(prov_path)
        self.assertEqual(size5, size7)
        size8 = self.check_size(prov_patha)
        self.assertEqual(size8, size6)

    def test_do_run(self):
        self.runsafe(self.do_run)
