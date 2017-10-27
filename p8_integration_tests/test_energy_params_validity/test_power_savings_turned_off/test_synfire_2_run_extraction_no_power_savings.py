"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
from testfixtures import LogCapture

nNeurons = 200  # number of neurons in each population
spike_times = [[0, 1050]]
run_times = [1000, 1000]
reset = False
synfire_run = TestRun()


class Synfire2RunExtractionIfCurrExp(BaseTestCase):
    def test_run(self):
        with LogCapture() as lc:
            synfire_run.do_run(nNeurons, spike_times=spike_times,
                               run_times=run_times, reset=False)
            self.assert_logs_messages(
                lc.records, "Working out if machine is booted", 'INFO', 1)


if __name__ == '__main__':
    synfire_run.do_run(
        nNeurons, spike_times=spike_times, run_times=run_times, reset=False)
