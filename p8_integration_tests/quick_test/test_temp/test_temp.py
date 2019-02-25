import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestTemp(BaseTestCase):

    def test_run1(self):
        sim.setup(timestep=1.0, n_chips_required=5)
        self.report("this is a new test", "run1")
        self.report("this is more stuff\n", "run1")
        sim.end()

    def test_run2(self):
        sim.setup(timestep=1.0, n_chips_required=5)
        self.report("this is another test\n", "run2")
        self.report("this is extra stuff", "run2a")
        sim.end()
