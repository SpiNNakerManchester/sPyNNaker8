import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoVertices(BaseTestCase):

    @staticmethod
    def test_run():
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        p.run(100)

        p.end()


if __name__ == '__main__':
    TestNoVertices.test_run()
