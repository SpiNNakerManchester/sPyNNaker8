"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils

n_neurons = 200  # number of neurons in each population
runtime = 5000
neurons_per_core = n_neurons / 2
record = False
record_v = True
record_gsyn = False
synfire_run = SynfireRunner()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=[runtime], record=record,
                           record_v=record_v, record_gsyn_exc=record_gsyn)
        gsyn = synfire_run.get_output_pop_gsyn_exc_list()
        v = synfire_run.get_output_pop_voltage_list()
        spikes = synfire_run.get_output_pop_spikes_list()

        self.assertEqual(1, len(v))
        self.assertEqual(0, len(gsyn))
        self.assertEqual(0, len(spikes))


if __name__ == '__main__':
    synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                       run_times=[runtime], record=record, record_v=record_v,
                       record_gsyn=record_gsyn)
    gsyn = synfire_run.get_output_pop_gsyn_exc_list()
    v = synfire_run.get_output_pop_voltage_numpy()
    spikes = synfire_run.get_output_pop_spikes_list()

    plot_utils.line_plot(v, title="v")
