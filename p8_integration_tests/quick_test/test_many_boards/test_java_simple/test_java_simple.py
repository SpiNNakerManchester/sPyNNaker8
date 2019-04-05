import time
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.manyBoards import ManyBoards


class TestPythonSimple(BaseTestCase):

    def do_run(self):
        me = ManyBoards()
        t_before = time.time()
        sim = me.do_run(n_boards=2, n_neurons=50, simtime=300)
        t_after_machine = time.time()
        me.check_all_data()
        t_after_check = time.time()
        results = self.get_run_time_of_BufferExtractor()
        self.report(
            results, "java_simple_n_boards=2_n_neurons=255_simtime=300")
        self.report(
            "machine run time was: {} seconds\n".format(
                t_after_machine-t_before),
            "java_simple_n_boards=2_n_neurons=255_simtime=300")
        self.report(
            "total run time was: {} seconds\n".format(t_after_check-t_before),
            "java_simple_n_boards=2_n_neurons=255_simtime=300")
        sim.end()

    def test_do_run(self):
        self.runsafe(self.do_run)
