import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestFailedState(BaseTestCase):

    def test_double_end(self):
        sim.setup(1.0)
        sim.end()
        sim.end()

    def test_only_end(self):
        sim.end()
