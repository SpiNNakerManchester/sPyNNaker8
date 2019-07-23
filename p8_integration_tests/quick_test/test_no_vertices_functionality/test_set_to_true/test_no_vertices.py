import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


class TestNoVertices(BaseTestCase):

    def do_run(self):
        p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        p.run(100)
        p.end()

    def test_run(self):
        self.runsafe(self.do_run)


if __name__ == '__main__':
    TestNoVertices.test_run()
