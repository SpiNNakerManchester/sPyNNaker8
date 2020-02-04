import math
import spynnaker8 as sim
from p8_integration_tests.quick_test.test_multitimestep.\
    multi_if_curr_exp_base import MultiIFCurrExpBase


def get_expected_spike_arrival(ssa_spike_time, ssa_timestep):
    # Calc when input sent spike
    input_spike_in_us = ssa_spike_time * 1000
    rounded_input_in_us = ssa_timestep * int(
        math.ceil(input_spike_in_us / ssa_timestep))

    # Spike sent by ssa at the end of the timestep
    return rounded_input_in_us + ssa_timestep


def get_expected_spike(index, estimate_arrival_in_us, delay, if_curr_timestep):
    # Arrive during an input timestep
    estimate_arrival_in_step = math.floor(
        estimate_arrival_in_us / if_curr_timestep)
    # this is to cover the time skuew
    if index < 2:
        estimate_arrival_in_step -= 1
    # Assumed to have actually been sent in the previous timestep
    # This could even be -1 if the ssa timestep is smaller than pop's
    calc_arrival_in_steps = estimate_arrival_in_step - 1
    calc_arrival_in_us = calc_arrival_in_steps * if_curr_timestep

    # round delay but always at least 1 timestep
    delay_timesteps = int(round((delay * 1000) / if_curr_timestep))
    if delay_timesteps < 1:
        delay_timesteps = 1
    delay_in_us = delay_timesteps * if_curr_timestep

    # 6000 is what I think the time to spike is
    calc_spike_in_us = calc_arrival_in_us + delay_in_us + 6000
    # round up to next timestep
    calc_spike_rounded = if_curr_timestep * int(
        math.ceil(calc_spike_in_us / if_curr_timestep))
    print(if_curr_timestep, calc_arrival_in_steps, calc_arrival_in_us,
          delay_in_us, calc_spike_in_us, calc_spike_rounded)
    return calc_spike_rounded / 1000


ssa_spike_time = 4
ssa_timestep = 2200
delay = 6
sim.setup(timestep=2)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 3)
input = sim.Population(
    1, sim.SpikeSourceArray([ssa_spike_time]), label="input",
    additional_parameters={"timestep_in_us": ssa_timestep}
)
input.record("spikes")
pop_1 = sim.Population(9, MultiIFCurrExpBase(), label="pop_1")
# pop_1 = sim.Population(9, sim.IF_curr_exp(), label="pop_1")
pop_1.record(["spikes", "v"])

proj = sim.Projection(input, pop_1, sim.AllToAllConnector(),
                      synapse_type=sim.StaticSynapse(weight=5, delay=delay))
sim.run(33)

proj.get("delay", "list")
i_neo = input.get_data(variables=["spikes"])
i_spikes = i_neo.segments[0].spiketrains
print(i_spikes)

neo = pop_1.get_data(variables="all")
spikes = neo.segments[0].spiketrains
print(spikes)
v = neo.segments[0].filter(name='v')[0]
print(v)
sim.end()

# Estimates do nto work due to the timeing sqews not sure worth fixing
estimate_arrival_in_us = get_expected_spike_arrival(
    ssa_spike_time, ssa_timestep)
print(estimate_arrival_in_us)
if_curr_timesteps = pop_1._vertex.timesteps_in_us
calc_spike_in_ms = []
for i in range(len(pop_1._vertex.timesteps_in_us)):
    calc_spike_in_ms.append(get_expected_spike(
        i, estimate_arrival_in_us, delay, if_curr_timesteps[i]))

print(calc_spike_in_ms)
