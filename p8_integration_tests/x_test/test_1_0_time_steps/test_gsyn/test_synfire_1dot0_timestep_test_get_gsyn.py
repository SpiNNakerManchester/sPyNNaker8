"""
Synfirechain-like example
"""
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
import spynnaker.gsyn_tools as gsyn_tools
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

n_neurons = 10  # number of neurons in each population
max_delay = 14.4
timestep = 1
neurons_per_core = n_neurons/2
delay = 1.7
runtime = 50
synfire_run = SynfireRunner()


class TestGetGsyn(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """
    def test_get_gsyn(self):
        synfire_run.do_run(n_neurons, max_delay=max_delay, time_step=timestep,
                           neurons_per_core=neurons_per_core, delay=delay,
                           run_times=[runtime])
        spikes = synfire_run.get_output_pop_spikes_numpy()
        gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
        self.assertEquals(12, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        gsyn_tools.check_sister_gysn(__file__, n_neurons, runtime, gsyn)


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, max_delay=max_delay, time_step=timestep,
                       neurons_per_core=neurons_per_core, delay=delay,
                       run_times=[runtime])
    gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_numpy()
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
    gsyn_tools.check_sister_gysn(__file__, n_neurons, runtime, gsyn)
