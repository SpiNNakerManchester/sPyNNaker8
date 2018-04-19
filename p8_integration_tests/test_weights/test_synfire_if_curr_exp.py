"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

nNeurons = 200  # number of neurons in each population
neurons_per_core = 10
delay = 17
run_times = [5000]
get_weights = True
synfire_run = SynfireRunner()


class SynfireIfCurr_exp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(nNeurons, neurons_per_core=neurons_per_core,
                           delay=delay, run_times=run_times,
                           get_weights=get_weights)
        spikes = synfire_run.get_output_pop_spikes_numpy()
        weights = synfire_run.get_weights()

        self.assertEquals(263, len(spikes))
        self.assertEquals(200, len(weights))
        spike_checker.synfire_spike_checker(spikes, nNeurons)


if __name__ == '__main__':
    synfire_run.do_run(nNeurons, neurons_per_core=neurons_per_core,
                       delay=delay, run_times=run_times,
                       get_weights=get_weights)
    spikes = synfire_run.get_output_pop_spikes_numpy()
    weights = synfire_run.get_weights()

    print(len(spikes))
    print(len(weights))
    plot_utils.plot_spikes(spikes)
