import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.manyBoards import ManyBoards


class TestPythonSimple(BaseTestCase):

    def test_run(self):
        me = ManyBoards()
        sim = me.do_run(n_boards=1, n_neurons=255, simtime=30)
        results = self.get_run_time_of_BufferExtractor()
        self.report(results, "python_simple")
        sim.end()
        pop = 1/0
