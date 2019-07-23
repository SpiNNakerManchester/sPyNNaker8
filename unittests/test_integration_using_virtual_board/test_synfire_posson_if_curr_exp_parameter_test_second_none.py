import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
run_times = [5000, 5000]
wrap_around = False
# parameters for population 1 first run
input_class = p.SpikeSourcePoisson
start_time = 0
duration = 5000.0
rate = 2.0
# parameters for population 2 first run
set_between_runs = [(1, 'duration', 0)]
extract_between_runs = False
record_input_spikes = True

synfire_run = SynfireRunner()


class TestSynfirePossonIfCurrExpParameterTestSecondNone(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """
    def test_synfire_posson_if_curr_exp_parameter_test_second_none(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=run_times,
                           use_wrap_around_connections=wrap_around,
                           input_class=input_class,
                           start_time=start_time, duration=duration, rate=rate,
                           extract_between_runs=extract_between_runs,
                           set_between_runs=set_between_runs,
                           record_input_spikes=record_input_spikes)


if __name__ == '__main__':
    x = TestSynfirePossonIfCurrExpParameterTestSecondNone(
        "test_synfire_posson_if_curr_exp_parameter_test_second_none")
    x.test_synfire_posson_if_curr_exp_parameter_test_second_none()
