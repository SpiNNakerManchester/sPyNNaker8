#!/usr/bin/python
"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

n_neurons = 200  # number of neurons in each population
neurons_per_core = n_neurons / 2
runtime = 5000
synfire_run = SynfireRunner()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime])
        spikes = synfire_run.get_output_pop_spikes_numpy()
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        self.assertEquals(263, len(spikes))
        synfire_run.get_output_pop_gsyn_exc_numpy()


if __name__ == '__main__':
    results = synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                                 run_times=[runtime])
    spikes = synfire_run.get_output_pop_spikes_numpy()
    v = synfire_run.get_output_pop_voltage_numpy()
    gsyn = synfire_run.get_output_pop_gsyn_exc_numpy()

    print len(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gsyn")
