import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from spinn_front_end_common.utilities.exceptions import ConfigurationException


class TestNoVertices(BaseTestCase):

    @staticmethod
    def test_run():
        try:
            p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
            p.run(100)

            p.end()
            raise Exception("failed to raise exception")
        except ConfigurationException:
            return


if __name__ == '__main__':
    TestNoVertices.test_run()
