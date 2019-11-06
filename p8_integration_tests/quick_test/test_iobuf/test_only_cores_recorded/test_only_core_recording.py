# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase
from pacman.model.constraints.placer_constraints import ChipAndCoreConstraint
from spinn_front_end_common.utilities import globals_variables


class TestOnlyCoresRecording(BaseTestCase):

    def do_run(self):
        # From the config file
        requested_cores = [(0, 0, 1), (0, 0, 3), (1, 1, 1)]
        sim.setup(timestep=1.0)
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

        machine = globals_variables.get_simulator().machine
        existing_chips = list()
        while len(existing_chips) < 2:
            for chip in machine.chips:
                existing_chips.append(chip)
        coords_first_chip = list()
        while len(coords_first_chip) < 2:
            chip = existing_chips[0]
            for processor_id in chip.processors:
                coords_first_chip.append([chip.x, chip.y, processor_id])
        coords_second_chip = list()
        while len(coords_first_chip) < 1:
            chip = existing_chips[1]
            for processor_id in chip.processors:
                coords_second_chip.append([chip.x, chip.y, processor_id])

        input = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]), label="input")
        input2 = sim.Population(
            1, sim.SpikeSourceArray(spike_times=[0]), label="input")
        coord1 = coords_first_chip[0]
        input.set_constraint(
            ChipAndCoreConstraint(coord1[0], coord1[1], coord1[2]))
        coord2 = coords_first_chip[1]
        input2.set_constraint(
            ChipAndCoreConstraint(coord2[0], coord2[1], coord2[2]))
        pop_1 = sim.Population(100, sim.IF_curr_exp(), label="pop_1")
        coord3 = coords_second_chip[0]
        pop_1.set_constraint(
            ChipAndCoreConstraint(coord3[0], coord3[1], coord3[2]))
        sim.Projection(input, pop_1, sim.AllToAllConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=18))
        sim.run(500)

        provenance_files = self.get_app_iobuf_files()
        sim.end()

        # extract_iobuf_from_cores = 0,0,1
        self.assertIn(
            "iobuf_for_chip_{}_{}_processor_id_{}.txt".format(
                coord1[0], coord1[1], coord1[2]), provenance_files)
        self.assertIn(
            "iobuf_for_chip_{}_{}_processor_id_{}.txt".format(
                coord2[0], coord2[1], coord2[2]), provenance_files)
        self.assertIn(
            "iobuf_for_chip_{}_{}_processor_id_{}.txt".format(
                coord3[0], coord3[1], coord3[2]), provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_4.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_5.txt", provenance_files)
        self.assertNotIn(
            "iobuf_for_chip_0_0_processor_id_6.txt", provenance_files)
        self.assertIn(
            "iobuf_for_chip_1_1_processor_id_1.txt", provenance_files)

    def test_do_run(self):
        self.runsafe(self.do_run)
