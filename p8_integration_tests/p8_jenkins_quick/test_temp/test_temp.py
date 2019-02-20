from os.path import expanduser
from spinn_front_end_common.utilities import globals_variables
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestTemp(BaseTestCase):

    def test_pop(self):
        sim.setup(timestep=1.0, n_chips_required=5)
        report_directory = globals_variables.get_simulator() \
            ._report_default_directory
        home = expanduser("~")
        print(report_directory)
        print(home)
        sim.end()
        pop = 1/0
