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

from __future__ import division
import math
from spinn_utilities.helpful_functions import lcm
import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase

class TestSimple(BaseTestCase):

    def do_script(self, sys_timestep, ssa_timestep, ssa_spike_time,
                  if_curr_timestep, delay, runtime):
        sim.setup(timestep=sys_timestep)

        input = sim.Population(
            1, sim.SpikeSourceArray([ssa_spike_time]), label="input",
            additional_parameters={"timestep_in_us": ssa_timestep})
        input.record("spikes")
        pop_1 = sim.Population(
            1, sim.IF_curr_exp(), label="pop_1",
            additional_parameters={"timestep_in_us": if_curr_timestep})
        pop_1.record(["spikes", "v"])

        sim.Projection(input, pop_1, sim.OneToOneConnector(),
                       synapse_type=sim.StaticSynapse(weight=5, delay=delay))
        sim.run(runtime)
        i_neo = input.get_data(variables=["spikes"])
        p_neo = pop_1.get_data(variables=["spikes", "v"])
        sim.end()

        # If specific was None the sys should have been used
        if ssa_timestep is None:
            ssa_timestep =  int(sys_timestep * 1000)
        if if_curr_timestep is None:
            if_curr_timestep = int(sys_timestep * 1000)

        # Calc when input sent spike
        input_spike_in_us = ssa_spike_time * 1000
        rounded_input_in_us =  ssa_timestep * int(
            math.ceil(input_spike_in_us/ssa_timestep))
        rounded_input_spike_in_ms = rounded_input_in_us / 1000

        # Spike sent by ssa at the end of the timestep
        estimate_arrival_in_us = rounded_input_in_us + ssa_timestep
        # Arrive during an input timestep
        estimate_arrival_in_step = math.floor(
            estimate_arrival_in_us / if_curr_timestep)
        # Assumed to have actually been sent in the previous timestep
        # This could even be -1 if the ssa timestep is smaller than pop's
        calc_arrival_in_steps  = estimate_arrival_in_step - 1
        calc_arrival_in_us = calc_arrival_in_steps * if_curr_timestep

        #round delay but always at least 1 timestep
        delay_timesteps = int(round((delay * 1000) / if_curr_timestep))
        if delay_timesteps < 1:
            delay_timesteps = 1
        delay_in_us = delay_timesteps * if_curr_timestep

        # 6000 is what I think the time to spike is
        calc_spike_in_us = calc_arrival_in_us + delay_in_us + 6000
        # round up to next timestep
        calc_spike_rounded = if_curr_timestep * int(
            math.ceil(calc_spike_in_us / if_curr_timestep))
        calc_spike_in_ms = calc_spike_rounded / 1000

        lcm_timestep = lcm(int(sys_timestep * 1000), ssa_timestep, if_curr_timestep)
        runtime_in_lcm = math.ceil(runtime * 1000 / lcm_timestep)
        runtime_in_us = runtime_in_lcm * lcm_timestep
        runtime_in_pop_timesteps = runtime_in_us / if_curr_timestep

        print(rounded_input_spike_in_ms, calc_arrival_in_us, delay_in_us,
              calc_spike_in_ms, runtime_in_pop_timesteps)
        i_spikes = i_neo.segments[0].spiketrains
        self.assertEquals(len(i_spikes), 1)
        self.assertAlmostEquals(float(i_spikes[0].magnitude), rounded_input_spike_in_ms)

        spikes = p_neo.segments[0].spiketrains
        # Spike sent timestgep after the 6 so 9. Pop spikes 6 steps later so 15
        self.assertAlmostEquals(float(spikes[0].magnitude), calc_spike_in_ms)
        v = p_neo.segments[0].filter(name='v')[0]
        # Runtime 20ms rounded up to next lcm timestep of 3000us so 21ms
        self.assertAlmostEquals(float(v.size), runtime_in_pop_timesteps)

    def do_complex(self):
        self.do_script(
            sys_timestep=1, ssa_timestep=2200, ssa_spike_time=5,
            if_curr_timestep=3100, delay=7, runtime=33)

    def test_complex(self):
        self.runsafe(self.do_complex)

    def do_pop_3000_4(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=1000, ssa_spike_time=0,
            if_curr_timestep=3000, delay=4, runtime=20)

    def test_pop_3000_4(self):
        self.runsafe(self.do_pop_3000_4)

    def do_pop_3000_5(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=1000, ssa_spike_time=0,
            if_curr_timestep=3000, delay=5, runtime=20)

    def test_pop_3000_5(self):
        self.runsafe(self.do_pop_3000_5)

    def do_pop_3000(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=1000, ssa_spike_time=0,
            if_curr_timestep=3000, delay=1, runtime=20)

    def test_pop_3000(self):
        self.runsafe(self.do_pop_3000)

    def do_ssa_3000_5(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=3000, ssa_spike_time=5,
            if_curr_timestep=1000, delay=1, runtime=20)

    def test_ssa_3000_5(self):
        self.runsafe(self.do_ssa_3000_5)

    def do_ssa_1000_6(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=1000, ssa_spike_time=6,
            if_curr_timestep=1000, delay=1, runtime=20)

    def test_ssa_1000_6(self):
        self.runsafe(self.do_ssa_1000_6)

    def do_none(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=None, ssa_spike_time=0,
            if_curr_timestep=None, delay=1, runtime=20)

    def test_none(self):
        self.runsafe(self.do_none)

    def do_simple(self):
        self.do_script(
            sys_timestep=1.0, ssa_timestep=1000, ssa_spike_time=0,
            if_curr_timestep=1000, delay=1, runtime=20)

    def test_simple(self):
        self.runsafe(self.do_simple)
