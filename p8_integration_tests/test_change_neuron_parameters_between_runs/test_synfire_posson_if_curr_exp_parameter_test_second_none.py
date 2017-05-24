from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson
import spynnaker.spike_checker as spike_checker
import spynnaker.plot_utils as plot_utils
import numpy

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
run_times = [5000, 5000]
wrap_around = False
# parameters for population 1 first run
input_class = SpikeSourcePoisson
start_time = 0
duration = 5000.0
rate = 2.0
# parameters for population 2 first run
set_between_runs = [(1, 'duration', 0)]
extract_between_runs = False
record_input_spikes = True

synfire_run = TestRun()


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
        input = synfire_run.get_spike_source_spikes()
        spikes = synfire_run.get_output_pop_spikes()
        # Check input spikes stop
        hist = numpy.histogram(input[:, 1], bins=[0, 5000, 10000])
        self.assertEqual(0, hist[0][1])
        spike_checker.synfire_multiple_lines_spike_checker(spikes, n_neurons,
                                                           len(input),
                                                           wrap_around=False)


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=run_times,
                       use_wrap_around_connections=wrap_around,
                       input_class=input_class, start_time=start_time,
                       duration=duration, rate=rate,
                       extract_between_runs=extract_between_runs,
                       set_between_runs=set_between_runs,
                       record_input_spikes=record_input_spikes)
    gsyn = synfire_run.get_output_pop_gsyn()
    v = synfire_run.get_output_pop_voltage()
    input = synfire_run.get_spike_source_spikes()
    hist = numpy.histogram(input[:, 1], bins=[0, 5000, 10000])
    print hist[0][0], hist[0][1]
    spikes = synfire_run.get_output_pop_spikes()
    plot_utils.plot_spikes(input, spikes2=spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
