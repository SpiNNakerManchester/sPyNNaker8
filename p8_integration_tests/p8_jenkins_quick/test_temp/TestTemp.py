from os.path import expanduser
from spinn_front_end_common.utilities import globals_variables
import spynnaker8 as sim
from p8_integration_scripts.base_test_case import BaseTestCase


class TestTemp(BaseTestCase):
    sim.setup(timestep=1.0)
    sim.run(1)
    report_directory = globals_variables.get_simulator() \
        ._report_default_directory
    home = expanduser("~")
    print(report_directory)
    print(home)
    sim.end()
    pop = 1/0
