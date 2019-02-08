#!/usr/bin/python
"""
Synfirechain-like example
"""
import os
from pacman.model.constraints.placer_constraints import (
    ChipAndCoreConstraint)
from spinn_front_end_common.utility_models import (
    DataSpeedUpPacketGatherMachineVertex)
from p8_integration_tests.base_test_case import BaseTestCase
from p8_integration_tests.scripts.synfire_run import SynfireRunner

nNeurons = 200  # number of neurons in each population
constraint = ChipAndCoreConstraint(1, 1)
delay = 1
neurons_per_core = 100
synfire_run = SynfireRunner()


class Synfire200n10pc2chipsWithNoDelaysSpikeRecording(BaseTestCase):

    def test_run(self):
        synfire_run.do_run(nNeurons, delay=delay,
                           neurons_per_core=neurons_per_core,
                           constraint=constraint)
        synfire_run.get_output_pop_all_list()
        report_folder = synfire_run.get_default_report_folder()
        file_path = os.path.join(
            report_folder,
            DataSpeedUpPacketGatherMachineVertex.REPORT_NAME)
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    synfire_run.do_run(nNeurons, delay=delay,
                       neurons_per_core=neurons_per_core,
                       constraint=constraint)
    synfire_run.get_output_pop_all_list()
    report_folder = synfire_run.get_default_report_folder()
    file_path = os.path.join(
        report_folder,
        DataSpeedUpPacketGatherMachineVertex.REPORT_NAME)
    if not os.path.exists(file_path):
        raise Exception("missing report!")
