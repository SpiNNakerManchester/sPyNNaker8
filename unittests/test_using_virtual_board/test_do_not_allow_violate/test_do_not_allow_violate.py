# general imports
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim


class TestDoNotAllowViolate(BaseTestCase):
    """
    Tests that running too fast needs to be specifically allowed
    """

    def test_do_not_allow_violate(self):
        with self.assertRaises(ConfigurationException):
            sim.setup()   # remember pynn default is 0.1
