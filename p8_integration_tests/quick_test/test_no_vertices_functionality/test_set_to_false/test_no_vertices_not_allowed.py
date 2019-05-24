from spinn_front_end_common.utilities.exceptions import ConfigurationException
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoVerticesNotAllowed(BaseTestCase):

    def test_exception_raise(self):
        with self.assertRaises(ConfigurationException):
            p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
            p.run(100)

            p.end()


if __name__ == '__main__':
    x = TestNoVerticesNotAllowed("test_exception_raise")
    x.test_exception_raise()
