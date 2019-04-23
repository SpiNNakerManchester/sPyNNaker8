"""
Synfirechain-like example
"""
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
runtimes = [526, 526, 526, 526, 526, 370]
extract_between_runs = False
synfire_run = SynfireRunner()


class Synfire1RunNoExtractionIfCurrExpMappedToAutoPause(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=runtimes,
                           extract_between_runs=extract_between_runs)
        spikes = synfire_run.get_output_pop_spikes_numpy()

        self.assertEqual(158, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=runtimes,
                       extract_between_runs=extract_between_runs)
    gsyn = synfire_run.get_output_pop_gsyn_exc()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_numpy()

    print(len(spikes))
    plot_utils.plot_spikes(spikes)
    plot_utils.line_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")