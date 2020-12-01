import spynnaker8 as p
import spinn_gym as gym

from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
import os
from spinn_front_end_common.utilities.globals_variables import get_simulator
from icub_utilities import *

# Parameter definition
runtime = 10000
# Build input SSP and output population
input_size = 2  # neurons
output_size = 200  # neurons
input_rate = 20  # Hz
# get head_positions and head_velocities from file (1000 samples)
base_dir = "./"
head_pos = np.loadtxt(os.path.join(
    base_dir, "normalised_head_positions_1000.csv"))
head_vel = np.loadtxt(os.path.join(
    base_dir, "normalised_head_velocities_1000.csv"))

# The values in the files are [0,1] when we really want [-1,1]; obtain this
# by multiplying by 2 and subtracting 1

head_pos = (head_pos * 2.0) - 1.0
head_vel = (head_vel * 2.0) - 1.0


# perfect eye positions and velocities are exactly out of phase with head
perfect_eye_pos = np.concatenate((head_pos[500:], head_pos[:500]))
perfect_eye_vel = np.concatenate((head_vel[500:], head_vel[:500]))

# TEST
# Report 4 points:
for i in [0, 250, 500, 750]:
    print("At {}: head pos {:4.6f}, head vel {:4.6f}, eye pos {:4.6f}, eye vel {:4.6f}".format(
        i, head_pos[i], head_vel[i], perfect_eye_pos[i], perfect_eye_vel[i]))

# build ICubVorEnv model pop
error_window_size = 10  # ms

# Setup
p.setup(timestep=1.0)

input_pop = p.Population(input_size, p.SpikeSourcePoisson(rate=input_rate))
output_pop = p.Population(output_size, p.SpikeSourcePoisson(rate=0))

# Instantiate venv
icub_vor_env_model = gym.ICubVorEnv(
    head_pos, head_vel, perfect_eye_vel, perfect_eye_pos, error_window_size,
    output_size)
icub_vor_env_pop = p.Population(input_size, icub_vor_env_model)

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
plt.savefig("spinngym_icub_vor_test.png")
plt.show()
