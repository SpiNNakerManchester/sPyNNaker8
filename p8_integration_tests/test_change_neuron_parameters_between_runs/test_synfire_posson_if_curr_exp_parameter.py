from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson
import spynnaker.plot_utils as plot_utils
import numpy

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
run_times = [5000, 5000]
# parameters for population 1 first run
input_class = SpikeSourcePoisson
start_time = 0
duration = 5000.0
rate = 2.0
# parameters for population 2 first run
set_between_runs = [(1, 'start', 5000),
                    (1, 'rate', 200.0),
                    (1, 'duration', 2000.0)]
extract_between_runs = False

synfire_run = TestRun()


class TestSynfirePossonIfCurrExpParameter(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """
    def test_synfire_posson_if_curr_exp_parameter(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=run_times, input_class=input_class,
                           start_time=start_time, duration=duration, rate=rate,
                           extract_between_runs=extract_between_runs,
                           set_between_runs=set_between_runs)
        spikes = synfire_run.get_output_pop_spikes()
        # Check spikes increase in second half by at least a factor of ten
        hist = numpy.histogram(spikes[:, 1], bins=[0, 5000, 10000])
        self.assertLess(hist[0][0] * 10, hist[0][1])


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=run_times, input_class=input_class,
                       start_time=start_time, duration=duration, rate=rate,
                       extract_between_runs=extract_between_runs,
                       set_between_runs=set_between_runs)
    gsyn = synfire_run.get_output_pop_gsyn()
    v = synfire_run.get_output_pop_voltage()
    spikes = synfire_run.get_output_pop_spikes()
    hist = numpy.histogram(spikes[:, 1], bins=[0, 5000, 10000])
    print hist[0][0], hist[0][1]
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
