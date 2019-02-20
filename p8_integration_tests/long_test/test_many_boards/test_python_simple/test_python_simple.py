from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.manyBoards import ManyBoards


class TestPythonSimple(BaseTestCase):

    def test_run(self):
        me = ManyBoards()
        sim = me.do_run(n_boards=10, n_neurons=2550, simtime=3000)
        results = self.get_run_time_of_BufferExtractor()
        self.report(
            results, "python_simple_n_boards=10_n_neurons=2550_simtime=3000")
        sim.end()
