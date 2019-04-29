"""
Synfirechain-like example
"""
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
from spynnaker8.utilities import neo_convertor, neo_compare
from spynnaker8.utilities.version_util import pynn8_syntax
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

nNeurons = 200  # number of neurons in each population
spike_times = [[0, 1050]]
neurons_per_core = nNeurons/2
runtimes = [1000, 2000]
reset = True
synfire_run = SynfireRunner()


class Synfire1RunReset1RunLargertRuntimeNoExtraction(BaseTestCase):
    def test_run(self):
        synfire_run.do_run(nNeurons, spike_times=spike_times, reset=reset,
                           run_times=runtimes,
                           neurons_per_core=neurons_per_core, get_all=True)
        neos = synfire_run.get_output_pop_all_list()
        spikes_0_0 = neo_convertor.convert_spikes(neos[0], 0)
        spikes_1_1 = neo_convertor.convert_spikes(neos[1], 1)
        self.assertEquals(53, len(spikes_0_0))
        self.assertEquals(156, len(spikes_1_1))
        spike_checker.synfire_spike_checker(spikes_0_0, nNeurons)
        spike_checker.synfire_multiple_lines_spike_checker(spikes_1_1,
                                                           nNeurons, 2)
        # v + gsyn_exc + gsyn_ihn = 3 (spikes not in analogsignalarrays
        if pynn8_syntax:
            self.assertEquals(3, len(neos[0].segments[0].analogsignalarrays))
            self.assertEquals(3, len(neos[1].segments[0].analogsignalarrays))
            self.assertEquals(3, len(neos[1].segments[1].analogsignalarrays))
        else:
            self.assertEquals(3, len(neos[0].segments[0].analogsignals))
            self.assertEquals(3, len(neos[1].segments[0].analogsignals))
            self.assertEquals(3, len(neos[1].segments[1].analogsignals))
        neo_compare.compare_segments(neos[0].segments[0], neos[1].segments[0])
        #   neo compare does all the compares so just some safety come once
        spikes_1_0 = neo_convertor.convert_spikes(neos[1], 0)
        for s1, s2 in zip(spikes_0_0, spikes_1_0):
            for (a1, a2) in zip(s1, s2):
                self.assertEquals(a1, a2)
        v_0_0 = neo_convertor.convert_data(neos[0], "v", 0)
        v_1_0 = neo_convertor.convert_data(neos[1], "v", 0)
        v_1_1 = neo_convertor.convert_data(neos[1], "v", 1)
        self.assertEquals(nNeurons*runtimes[0], len(v_0_0))
        self.assertEquals(nNeurons*runtimes[0], len(v_1_0))
        self.assertEquals(nNeurons*runtimes[1], len(v_1_1))
        gsyn_exc_0_0 = neo_convertor.convert_data(neos[0], "gsyn_exc", 0)
        gsyn_exc_1_0 = neo_convertor.convert_data(neos[1], "gsyn_exc", 0)
        gsyn_exc_1_1 = neo_convertor.convert_data(neos[1], "gsyn_exc", 1)
        self.assertEquals(nNeurons*runtimes[0], len(gsyn_exc_0_0))
        self.assertEquals(nNeurons*runtimes[0], len(gsyn_exc_1_0))
        self.assertEquals(nNeurons*runtimes[1], len(gsyn_exc_1_1))
        gsyn_inh_0_0 = neo_convertor.convert_data(neos[0], "gsyn_inh", 0)
        gsyn_inh_1_0 = neo_convertor.convert_data(neos[1], "gsyn_inh", 0)
        gsyn_inh_1_1 = neo_convertor.convert_data(neos[1], "gsyn_inh", 1)
        self.assertEquals(nNeurons*runtimes[0], len(gsyn_inh_0_0))
        self.assertEquals(nNeurons*runtimes[0], len(gsyn_inh_1_0))
        self.assertEquals(nNeurons*runtimes[1], len(gsyn_inh_1_1))


if __name__ == '__main__':
    synfire_run.do_run(nNeurons, spike_times=spike_times, reset=reset,
                       run_times=runtimes, neurons_per_core=neurons_per_core,
                       get_all=True)
    neos = synfire_run.get_output_pop_all_list()
    spikes = [1, 1]
    spikes[0] = neo_convertor.convert_spikes(neos[1], 0)
    spikes[1] = neo_convertor.convert_spikes(neos[1], 1)
    v_1_0 = neo_convertor.convert_data(neos[1], "v", 0)
    v_1_1 = neo_convertor.convert_data(neos[1], "v", 1)
    gsyn_exc_1_0 = neo_convertor.convert_data(neos[1], "gsyn_exc", 0)
    gsyn_exc_1_1 = neo_convertor.convert_data(neos[1], "gsyn_exc", 1)
    print(len(spikes[0]))
    print(len(spikes[1]))
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v_1_0, title="v1")
    plot_utils.heat_plot(gsyn_exc_1_0, title="gysn1")
    plot_utils.heat_plot(v_1_1, title="v2")
    plot_utils.heat_plot(gsyn_exc_1_1, title="gysn2")
