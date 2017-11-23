from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import TestRun
import spynnaker.plot_utils as plot_utils
import numpy

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
runtimes = [5000, 5000]
set_between_runs = [(0, 'i_offset', 30)]
synfire_run = TestRun()
extract_between_runs = False


class TestGetGsyn(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """
    def test_get_gsyn(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=runtimes,
                           extract_between_runs=extract_between_runs,
                           set_between_runs=set_between_runs)
        spikes = synfire_run.get_output_pop_spikes_numpy()
        # Check spikes increase in second half by at least a factor of ten
        hist = numpy.histogram(spikes[:, 1], bins=[0, 5000, 10000])
        self.assertEquals(263, hist[0][0])
        self.assertEquals(333400, hist[0][1])


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=runtimes,
                       extract_between_runs=extract_between_runs,
                       set_between_runs=set_between_runs)
    gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_numpy()
    hist = numpy.histogram(spikes[:, 1], bins=[0, 5000, 10000])
    print hist[0][0], hist[0][1]
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
