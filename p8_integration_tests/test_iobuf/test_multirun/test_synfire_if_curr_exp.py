"""
Synfirechain-like example
"""
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
import spynnaker.plot_utils as plot_utils
from spynnaker8.utilities import neo_convertor
import spynnaker.spike_checker as spike_checker

n_neurons = 200  # number of neurons in each population
runtimes = [1000, 1000, 1000, 1000, 1000]
neurons_per_core = n_neurons / 2
synfire_run = SynfireRunner()


class SynfireIfCurrExp(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                           run_times=runtimes, record=True, record_v=True,
                           record_gsyn_exc=True, record_gsyn_inh=False)
        spikes_neos = synfire_run.get_output_pop_spikes_list()

        len0 = reduce(lambda x, y: x + y,
                      map(len, spikes_neos[0].segments[0].spiketrains))
        len1 = reduce(lambda x, y: x + y,
                      map(len, spikes_neos[1].segments[0].spiketrains))
        len2 = reduce(lambda x, y: x + y,
                      map(len, spikes_neos[2].segments[0].spiketrains))
        len3 = reduce(lambda x, y: x + y,
                      map(len, spikes_neos[3].segments[0].spiketrains))
        len4 = reduce(lambda x, y: x + y,
                      map(len, spikes_neos[4].segments[0].spiketrains))
        self.assertEquals(53, len0)
        self.assertEquals(106, len1)
        self.assertEquals(158, len2)
        self.assertEquals(211, len3)
        self.assertEquals(263, len4)
        spikes = map(neo_convertor.convert_spikes, spikes_neos)
        spike_checker.synfire_spike_checker(spikes, n_neurons)


if __name__ == '__main__':
    results = synfire_run.do_run(n_neurons, neurons_per_core=neurons_per_core,
                                 run_times=runtimes, record=True,
                                 record_v=True, record_gsyn_exc=True,
                                 record_gsyn_inh=False)
    # TODO plotting if required
    # gsyn = synfire_run.get_output_pop_gsyn()
    # v = synfire_run.get_output_pop_voltage()
    spikes_neos = synfire_run.get_output_pop_spikes_list()
    len0 = reduce(lambda x, y: x + y,
                  map(len, spikes_neos[0].segments[0].spiketrains))
    len1 = reduce(lambda x, y: x + y,
                  map(len, spikes_neos[1].segments[0].spiketrains))
    len2 = reduce(lambda x, y: x + y,
                  map(len, spikes_neos[2].segments[0].spiketrains))
    len3 = reduce(lambda x, y: x + y,
                  map(len, spikes_neos[3].segments[0].spiketrains))
    len4 = reduce(lambda x, y: x + y,
                  map(len, spikes_neos[4].segments[0].spiketrains))
    print len0, len1, len2, len3, len4

    spikes = map(neo_convertor.convert_spikes, spikes_neos)
    plot_utils.plot_spikes(spikes)
    # plot_utils.heat_plot(v, title="v")
    # plot_utils.heat_plot(gsyn, title="gsyn")
