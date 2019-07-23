import time
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.manyBoards import ManyBoards


class TestJavaAdvanced(BaseTestCase):

    def do_run(self):
        me = ManyBoards()
        t_before = time.time()
        sim = me.do_run(n_boards=10, n_neurons=2550, simtime=3000)
        t_after = time.time()
        results = self.get_run_time_of_BufferExtractor()
        self.report(
            results, "java_simple_n_boards=10_n_neurons=2550_simtime=3000")
        self.report(
            "total run time was: {} seconds".format(t_after-t_before),
            "java_simple_n_boards=10_n_neurons=2550_simtime=3000")
        sim.end()

    def test_do_run(self):
        self.runsafe(self.do_run)
