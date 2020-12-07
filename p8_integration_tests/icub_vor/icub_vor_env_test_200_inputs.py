import spynnaker8 as p
import spinn_gym as gym

from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
import os
from spinn_front_end_common.utilities.globals_variables import get_simulator
from icub_utilities import *

# Parameter definition
runtime = 2000
# Build input SSP and output population
input_size = 200  # neurons
output_size = 200  # neurons

input_spike_times = [[] for _ in range(input_size)]

for i in range(5):
    input_spike_times[i*2] = [250+(10 * 2 *  i) for _ in range(1)]
    input_spike_times[2*i+1] = [500+(10 * (2 * i+1)) for _ in range(1)]
    input_spike_times[50 + i*2] = [750+(10 * 2 *  i) for _ in range(100+i)]
    input_spike_times[100 + 2*i+1] = [1000+(10 * (2 * i+1)) for _ in range(100+i)]
    input_spike_times[150 + i*2] = [1250+(10 * 2 *  i) for _ in range(1000+i)]
    input_spike_times[150 + 2*i+1] = [1500+(10 * (2 * i+1)) for _ in range(1000+i)]

head_pos, head_vel = generate_head_position_and_velocity(1)

# perfect eye positions and velocities are exactly out of phase with head
perfect_eye_pos = np.concatenate((head_pos[500:], head_pos[:500]))
perfect_eye_vel = np.concatenate((head_vel[500:], head_vel[:500]))

# build ICubVorEnv model pop
error_window_size = 10  # ms

# Setup
p.setup(timestep=1.0)
p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 50)
p.set_number_of_neurons_per_core(p.SpikeSourceArray, 50)
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
errors = get_error(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
l_counts = get_l_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
r_counts = get_r_count(icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
rec_head_pos = get_head_pos(
    icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)
rec_head_vel = get_head_vel(
    icub_vor_env_pop=icub_vor_env_pop, simulator=simulator)

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
plt.plot(x_plot, rec_head_pos, label="head position")
plt.plot(x_plot, rec_head_vel, label="head velocity")
# plt.plot(perfect_eye_pos, label="eye position", ls='--')
# plt.plot(perfect_eye_vel, label="eye velocity", ls='--')
plt.legend(loc="best")
plt.xlim([0, runtime])

plt.subplot(5, 1, 4)
plt.plot(x_plot, errors, label="errors")
plt.legend(loc="best")
plt.xlim([0, runtime])

plt.subplot(5, 1, 5)
plt.scatter(
    [i[1] for i in spikes_out_spin], [i[0] for i in spikes_out_spin], s=1)
plt.legend(loc="best")
plt.xlim([0, runtime])
plt.savefig("spinngym_icub_vor_test_200_neurons.png")
# plt.show()