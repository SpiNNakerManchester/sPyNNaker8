import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.manyBoards import ManyBoards


class TestPythonAdvanced(BaseTestCase):

    def test_run(self):
        me = ManyBoards()
        sim = me.do_run(n_boards=2, n_neurons=255, simtime=300)
        results = self.get_run_time_of_BufferExtractor()
        self.report(results, "python_advanced")
        sim.end()
