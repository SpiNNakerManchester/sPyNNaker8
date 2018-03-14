#!/usr/bin/python
"""
Synfirechain-like example
"""

from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner
from pacman.model.constraints.placer_constraints \
    import RadialPlacementFromChipConstraint

import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

nNeurons = 200  # number of neurons in each population
constraint = RadialPlacementFromChipConstraint(3, 3)
delay = 1
neurons_per_core = 10
record_v = False
record_gsyn = False
synfire_run = SynfireRunner()


class Synfire200n10pc2chipsWithNoDelaysSpikeRecording(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(nNeurons, delay=delay,
                           neurons_per_core=neurons_per_core,
                           constraint=constraint, record_v=record_v,
                           record_gsyn_exc=record_gsyn,
                           record_gsyn_inh=record_gsyn)
        spikes = synfire_run.get_output_pop_spikes_numpy()

        self.assertEquals(333, len(spikes))
        spike_checker.synfire_spike_checker(spikes, nNeurons)


if __name__ == '__main__':
    synfire_run.do_run(nNeurons, delay=delay,
                       neurons_per_core=neurons_per_core,
                       constraint=constraint, record_v=record_v,
                       record_gsyn_exc=record_gsyn,
                       record_gsyn_inh=record_gsyn)
    spikes = synfire_run.get_output_pop_spikes_numpy()

    print len(spikes)
    plot_utils.plot_spikes(spikes)
    # v and gysn are None
