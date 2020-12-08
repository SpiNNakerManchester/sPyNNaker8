import spynnaker8 as p
import spinn_gym as gym

from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
import os
from spinn_front_end_common.utilities.globals_variables import get_simulator
from icub_utilities import *

# Parameter definition
runtime = 5000
# Build input SSP and output population
input_size = 200  # neurons
output_size = 200  # neurons
gain = 20.0

head_pos, head_vel = generate_head_position_and_velocity(1)

# perfect eye positions and velocities are exactly out of phase with head
perfect_eye_pos = np.concatenate((head_pos[500:], head_pos[:500]))
perfect_eye_vel = np.concatenate((head_vel[500:], head_vel[:500]))

error_window_size = 10  # ms
npc_limit = 50
input_spike_times = [[] for _ in range(input_size)]

for i in range(5):
    input_spike_times[i * 2] = [250 + (10 * 2 * i) for _ in range(1)]
    input_spike_times[2 * i + 1] = [500 + (10 * (2 * i + 1)) for _ in range(1)]
    input_spike_times[50 + i * 2] = [750 + (10 * 2 * i) for _ in range(10 + i)]
    input_spike_times[100 + 2 * i + 1] = [1000 + (10 * (2 * i + 1)) for _ in range(10 + i)]
    input_spike_times[150 + i * 2] = [1250 + (10 * 2 * i) for _ in range(100 + i)]
    input_spike_times[150 + 2 * i + 1] = [1500 + (10 * (2 * i + 1)) for _ in range(100 + i)]

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
results = retrieve_and_package_results(icub_vor_env_pop, simulator)

# get the spike data from input and output
spikes_in_spin = input_pop.spinnaker_get_data('spikes')
spikes_out_spin = output_pop.spinnaker_get_data('spikes')

# end simulation
p.end()

remapped_vn_spikes = remap_odd_even(spikes_in_spin, input_size)
remapped_cf_spikes = remap_second_half_descending(spikes_out_spin, output_size)

simulation_parameters = {
    'runtime': runtime,
    'error_window_size': error_window_size,
    'vn_spikes': remapped_vn_spikes,
    'cf_spikes': remapped_cf_spikes,
    'perfect_eye_pos': perfect_eye_pos,
    'perfect_eye_vel': perfect_eye_vel,
    'vn_size': input_size,
    'cf_size': output_size,
    'gain': gain
}

# plot the data from the ICubVorEnv pop
plot_results(results_dict=results, simulation_parameters=simulation_parameters,
             name="spinngym_icub_vor_test_200_inputs")

print("Done")
