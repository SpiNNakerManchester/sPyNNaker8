"""
Synfirechain-like example
"""
from unittest import SkipTest
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestOnlyCoresRecording(BaseTestCase):

    def test_run(self):
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

        input = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]),
                               label="input")
        pop_1 = sim.Population(200, sim.IF_curr_exp(), label="pop_1")
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=18))
        sim.run(500)

        provenance_files = self.get_provenance_files()
        sim.end()

        # extract_iobuf_from_cores = 0,0,1
        self.assertIn(
            "iobuf_for_chip_0_0_processor_id_1.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_2.txt", provenance_files)
        self.assertIn(
            "iobuf_for_chip_0_0_processor_id_3.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_4.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_5.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_6.txt", provenance_files)
        self.assertIn(
            "iobuf_for_chip_1_1_processor_id_1.txt", provenance_files)
