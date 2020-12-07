import spynnaker8 as p
import spinn_gym as gym

from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
import os
from spinn_front_end_common.utilities.globals_variables import get_simulator
from icub_utilities import *

# Parameter definition
runtime = 3000
# Build input SSP and output population
input_size = 200  # neurons
output_size = 200  # neurons
gain = 20.0

head_pos, head_vel = generate_head_position_and_velocity(1)

# perfect eye positions and velocities are exactly out of phase with head
perfect_eye_pos = np.concatenate((head_pos[500:], head_pos[:500]))
perfect_eye_vel = np.concatenate((head_vel[500:], head_vel[:500]))

input_spike_times = [[] for _ in range(input_size)]
# the constant number (0.000031) is the effect of a single spike on the head position
# assert (np.isclose(np.abs(np.diff(head_pos)[0]), no_required_spikes_per_chunk * 0.000031), 0.001)
sub_head_pos = np.diff(head_pos)
head_movement_per_spike = 2 ** (-15) * gain
sub_eye_pos = np.concatenate(([0], np.diff(perfect_eye_pos)))

# no_required_spikes_per_chunk = 200
no_required_spikes_per_chunk = np.ceil(np.abs(sub_head_pos[0]) / head_movement_per_spike)

# build ICubVorEnv model pop
error_window_size = 10  # ms
npc_limit = 25
no_input_cores = int(input_size / npc_limit)
for ts in range(runtime - 1):
    spikes_during_chunk = np.ceil(sub_eye_pos[ts % 1000] / head_movement_per_spike)
    for i in range(int(np.abs(spikes_during_chunk))):
        x = int(spikes_during_chunk <= 0)
        input_spike_times[(i % no_input_cores) * npc_limit + x].append(ts)

# Setup
p.setup(timestep=1.0)
p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 50)
p.set_number_of_neurons_per_core(p.SpikeSourceArray, npc_limit)
input_pop = p.Population(input_size, p.SpikeSourceArray(spike_times=input_spike_times))

output_pop = p.Population(output_size, p.SpikeSourcePoisson(rate=0))

# Instantiate venv
icub_vor_env_model = gym.ICubVorEnv(
    head_pos, head_vel, perfect_eye_vel, perfect_eye_pos, error_window_size,
    output_size)
icub_vor_env_pop = p.Population(ICUB_VOR_VENV_POP_SIZE, icub_vor_env_model)

# Set recording for input and output pop (env pop records by default)
input_pop.record('spikes')
output_pop.record('spikes')

# Input -> ICubVorEnv projection
i2a = p.Projection(input_pop, icub_vor_env_pop, p.AllToAllConnector())

# ICubVorEnv -> output, setup live output to the SSP vertex
p.external_devices.activate_live_output_to(
    icub_vor_env_pop, output_pop, "CONTROL")

# Store simulator and run
simulator = get_simulator()
# Run the simulation
p.run(runtime)

# Get the data from the ICubVorEnv pop
errors = np.asarray(get_error(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator))
l_counts = get_l_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
r_counts = get_r_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
rec_head_pos = np.asarray(get_head_pos(
    icub_vor_env_pop=icub_vor_env_pop, simulator=simulator))
rec_head_vel = np.asarray(get_head_vel(
    icub_vor_env_pop=icub_vor_env_pop, simulator=simulator))

# get the spike data from input and output and plot
# spikes_in = input_pop.get_data('spikes').segments[0].spiketrains
# spikes_out = output_pop.get_data('spikes').segments[0].spiketrains
# Figure(
#     Panel(spikes_in, xlabel="Time (ms)", ylabel="nID",
#           xticks=True, yticks=True),
#     Panel(spikes_out, xlabel="Time (ms)", ylabel="nID",
#           xticks=True, yticks=True)
# )
# plt.show()

spikes_in_spin = input_pop.spinnaker_get_data('spikes')
spikes_out_spin = output_pop.spinnaker_get_data('spikes')

# end simulation
p.end()

# plot the data from the ICubVorEnv pop
x_plot = [(n) for n in range(0, runtime, error_window_size)]
plt.figure(figsize=(15, 11), dpi=300)
plt.subplot(5, 1, 1)
plt.scatter(
    [i[1] for i in spikes_in_spin], [i[0] for i in spikes_in_spin], s=1)
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.subplot(5, 1, 2)
plt.plot(x_plot, l_counts, 'bo', label="l_counts")
plt.plot(x_plot, r_counts, 'ro', label="r_counts")
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.subplot(5, 1, 3)
plt.plot(x_plot, rec_head_pos, label="rec. eye position")
plt.plot(x_plot, rec_head_vel, label="rec. eye velocity")
plt.plot(np.tile(perfect_eye_pos, runtime // 1000), label="eye position", ls=':')
plt.plot(np.tile(perfect_eye_vel, runtime // 1000), label="eye velocity", ls=':')
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.subplot(5, 1, 4)
plt.plot(x_plot, errors, label="rec. error")
plt.plot(x_plot, np.tile(perfect_eye_pos[::error_window_size], runtime // 1000) - rec_head_pos.ravel(),
         label="eye position diff")
plt.plot(x_plot, np.tile(perfect_eye_vel[::error_window_size], runtime // 1000) - rec_head_vel.ravel(),
         label="eye velocity diff")
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.subplot(5, 1, 5)
plt.scatter(
    [i[1] for i in spikes_out_spin], [i[0] for i in spikes_out_spin], s=1)
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.savefig("spinngym_icub_vor_test_perfect.png")
# plt.show()

print("Done")
