# Standard library imports
import cPickle as pickle
import time
import numpy as np
import os
import errno
import matplotlib.pyplot as plt
import random

# Third party imports
import spynnaker8 as p

# Local application imports
import utilities as util
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.space import Grid2D, Line
from pyNN.utility.plotting import Figure, Panel
import random_walk_any_dir

"""
SETUP
"""
p.setup(1)  # simulation timestep (ms)
runtime = 100  # ms

n_row = 50
n_col = 50
n_neurons = n_row * n_row
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

self_connections = False  # allow self-connections in recurrent grid cell network

rng = NumpyRNG(seed=77364, parallel_safe=True)
synaptic_weight = 0.1  # synaptic weight for inhibitory connections
synaptic_radius = 10.0  # inhibitory connection radius
orientation_pref_shift = 2  # number of neurons to shift centre of connectivity by

# Grid cell (excitatory) population
gc_neuron_params = {
    "v_thresh": -50.0,
    "v_reset": -65.0,
    "v_rest": -65.0,
    "i_offset": 0.8,  # DC input
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1.0,
}

exc_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0, y0=0, z=0, fill_order='sequential')
# exc_space = p.Space(axes='xy', periodic_boundaries=((-n_col / 2, n_col / 2), (-n_row / 2, n_row / 2)))
v_init = RandomDistribution('uniform', low=-65, high=-55, rng=rng)
pop_exc_gc = p.Population(n_row * n_col,
                          p.IF_curr_exp(**gc_neuron_params),
                          cellparams=None,
                          initial_values={'v': v_init},
                          structure=exc_grid,
                          label="Excitatory grid cells"
                          )

# Create views
# view_exc = p.PopulationView(pop_exc, np.array([0, 1, n_col, n_col + 1]))  # view of 4 neurons
index_north_cells = list()
index_east_cells = list()
index_west_cells = list()
index_south_cells = list()

# Create recurrent inhibitory connections
loop_connections = list()
for pre_syn in range(0, n_row * n_col):
    presyn_pos = (pop_exc_gc.positions[pre_syn])[:2]
    dir_pref = np.array(util.get_dir_pref(presyn_pos))

    # Shift centre of connectivity in appropriate direction
    shifted_centre = util.shift_centre_connectivity(presyn_pos, dir_pref, orientation_pref_shift, n_row, n_col)
    for post_syn in range(0, n_row * n_col):
        # If different neurons
        if pre_syn != post_syn or self_connections:
            postsyn_pos = (pop_exc_gc.positions[post_syn])[:2]
            dist = util.get_neuron_distance_periodic(n_col, n_row, shifted_centre, postsyn_pos)

            # Establish connection
            if np.all(dist <= synaptic_radius):
                # delay = util.normalise(dist, 1, 5)
                delay = 1.0
                singleConnection = (pre_syn, post_syn, synaptic_weight, delay)
                loop_connections.append(singleConnection)

# Create inhibitory connections
proj_exc = p.Projection(
    pop_exc_gc, pop_exc_gc, p.FromListConnector(loop_connections, ('weight', 'delay')),
    p.StaticSynapse(),
    receptor_type='inhibitory',
    label="Excitatory grid cells inhibitory connections")

# Input population encoding speed and head direction
# 0: N
# 1: E
# 2: W
# 3: S
input_structure = Line(dx=1.0, x0=0.0, y=0.0, z=0.0)
input_loop_connections = list()
pop_vel_input = p.Population(4,
                             p.SpikeSourcePoisson(rate=[0, 0, 0, 0], start=0, duration=runtime),
                             structure=input_structure,
                             label="Poisson input velocity cells")
pop_vel_input_n = p.PopulationView(pop_vel_input, 0)
pop_vel_input_s = p.PopulationView(pop_vel_input, 3)
pop_vel_input_e = p.PopulationView(pop_vel_input, 1)
pop_vel_input_w = p.PopulationView(pop_vel_input, 2)

# Connect input neuron to grid cells of appropriate direction
synaptic_weight_vel_input = 1.0
vel_input_delay = 1.0
for i, neuron_pos in enumerate(pop_exc_gc.positions):
    neuron_pos = neuron_pos[:2]
    neuron_pref_dir = util.get_dir_pref(neuron_pos)
    if np.all(neuron_pref_dir == [0, 1]):
        single_connection = (0, i, synaptic_weight_vel_input, vel_input_delay)
        index_north_cells.append(i)
    elif np.all(neuron_pref_dir == [0, -1]):
        single_connection = (3, i, synaptic_weight_vel_input, 1.0)
        index_south_cells.append(i)
    elif np.all(neuron_pref_dir == [1, 0]):
        single_connection = (1, i, synaptic_weight_vel_input, 1.0)
        index_east_cells.append(i)
    elif np.all(neuron_pref_dir == [-1, 0]):
        single_connection = (2, i, synaptic_weight_vel_input, 1.0)
        index_west_cells.append(i)
    input_loop_connections.append(single_connection)

view_exc_north = p.PopulationView(pop_exc_gc, index_north_cells)
view_exc_east = p.PopulationView(pop_exc_gc, index_east_cells)
view_exc_west = p.PopulationView(pop_exc_gc, index_west_cells)
view_exc_south = p.PopulationView(pop_exc_gc, index_south_cells)

proj_input = p.Projection(
    pop_vel_input, pop_exc_gc, p.FromListConnector(input_loop_connections, ('weight', 'delay')),
    receptor_type="excitatory",
    synapse_type=p.StaticSynapse(),
    label="Velocity input cells excitatory connections to appropriate grid cells"
)

"""
RUN
"""
pop_exc_gc.record(['v', 'gsyn_inh', 'gsyn_exc', 'spikes'])
pop_vel_input.record(["spikes"])

vel_input_rate = 100
agent_speed = 2  # m/s
vel_timestep = 100  # ms
env_size = 200  # cm
random_walk = random_walk_any_dir.RandomWalkAny(agent_speed, vel_timestep, env_size, env_size)
largest_change_xy = random_walk.get_stepsize()

for i in range(runtime / vel_timestep):
    step = random_walk.get_velocity()
    ns_weight = util.normalise(step.change_y, 0, largest_change_xy)
    we_weight = util.normalise(step.change_x, 0, largest_change_xy)

    # Update velocity input rates
    if step.head_dir == [0, 1]:
        pop_vel_input_n.set(rate=vel_input_rate*ns_weight)
    elif step.head_dir == [0, -1]:
        pop_vel_input_s.set(rate=vel_input_rate*ns_weight)

    if step.head_dir == [1, 0]:
        pop_vel_input_e.set(rate=vel_input_rate*we_weight)
    elif step.head_dir == [-1, 0]:
        pop_vel_input_w.set(rate=vel_input_rate*we_weight)

    p.run_until(i * vel_timestep)


"""
WRITE DATA
"""

# Write data to files
data_dir = "data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"

# Create directory
try:
    os.makedirs(os.path.dirname(data_dir))
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise

# Excitatory population
# pickle.dump(pop_exc.get_data().segments[0].filter(name='v')[0],
#             open(data_dir + "pop_exc_v.pkl", 'wb'),
#             protocol=pickle.HIGHEST_PROTOCOL)
# pickle.dump(pop_exc.get_data().segments[0].filter(name='gsyn_exc')[0],
#             open(data_dir + "pop_exc_gsyn_exc.pkl", 'wb'),
#             protocol=pickle.HIGHEST_PROTOCOL)
# pickle.dump(pop_exc.get_data().segments[0].filter(name='gsyn_inh')[0],
#             open(data_dir + "pop_exc_gsyn_inh.pkl", 'wb'),
#             protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_exc_gc.get_data().segments[0].spiketrains,
            open(data_dir + "pop_exc_gc_spiketrains.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_exc_gc.label, open(data_dir + "pop_exc_gc_label.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_exc_gc.positions, open(data_dir + "pop_exc_gc_positions.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(gc_neuron_params, open(data_dir + "pop_exc_gc_parameters.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

f = open(data_dir + "params.txt", "w")
f.write("Single population grid cell (periodic) model")
f.write("\nruntime=" + str(runtime))
f.write("\nn_row=" + str(n_row))
f.write("\nn_col=" + str(n_col))
f.write("\nsyn_weight=" + str(synaptic_weight))
f.write("\nsyn_radius=" + str(synaptic_radius))
f.write("\norientation_pref_shift=" + str(orientation_pref_shift))
f.write("\npop_exc=" + str(pop_exc_gc.describe()))
f.close()

rand_neurons = random.sample(range(0, n_neurons), 4)
neuron_sample = p.PopulationView(pop_exc_gc, rand_neurons)

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    # Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_inh')[0],
    #       ylabel="inhibitory synaptic conduction (uS)",
    #       xlabel="Time (ms)",
    #       data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    # Panel(neuron_sample.get_data().segments[0].spiketrains,
    #       yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
    #       ),
)
plt.savefig(data_dir + "sample_v.eps", format='eps')
plt.show()

F = Figure(
    # plot data for postsynaptic neuron
    # Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
    #       ylabel="Membrane potential (mV)",
    #       xlabel="Time (ms)",
    #       data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_inh')[0],
          ylabel="inhibitory synaptic conduction (nA)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    # Panel(neuron_sample.get_data().segments[0].spiketrains,
    #       yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
    #       ),
)
plt.savefig(data_dir + "sample_gsyn_inh.eps", format='eps')
plt.show()

F = Figure(
    # plot data for postsynaptic neuron
    # Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
    #       ylabel="Membrane potential (mV)",
    #       xlabel="Time (ms)",
    #       data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_exc')[0],
          ylabel="excitatory synaptic conduction (nA)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    # Panel(neuron_sample.get_data().segments[0].spiketrains,
    #       yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
    #       ),
)
plt.savefig(data_dir + "sample_gsyn_inh.eps", format='eps')
plt.show()


F = Figure(
    # plot data for postsynaptic neuron
    # Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
    #       ylabel="Membrane potential (mV)",
    #       xlabel="Time (ms)",
    #       data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    # Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_inh')[0],
    #       ylabel="inhibitory synaptic conduction (uS)",
    #       xlabel="Time (ms)",
    #       data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    Panel(neuron_sample.get_data().segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)
rand_neurons = map(str, rand_neurons)
plt.yticks(np.arange(4), rand_neurons)
plt.savefig(data_dir + "sample_spikes.eps", format='eps')
plt.show()

# Plot trajectory
trajectory = random_walk.get_trajectory(runtime)
pickle.dump(trajectory, open(data_dir + "trajectory.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
util.plot_trajectory_2d(np.array(trajectory), env_size, env_size, data_dir)

gsyn_inh = pop_exc_gc.get_data().segments[0].filter(name='gsyn_inh')[0]
gsyn_exc = pop_exc_gc.get_data().segments[0].filter(name='gsyn_exc')[0]
print("Max gsyn_inh=" + str(util.get_max_value_from_pop(gsyn_inh)))
print("Avg gsyn_inh=" + str(util.get_avg_gsyn_from_pop(gsyn_inh)))
print("Max gsyn_exc=" + str(util.get_max_value_from_pop(gsyn_exc)))
print("Avg gsyn_exc=" + str(util.get_avg_gsyn_from_pop(gsyn_exc)))
print("Mean spike count: " + str(pop_exc_gc.mean_spike_count(gather=True)))
print("Max spike count: " + str(util.get_max_firing_rate(pop_exc_gc.get_data().segments[0].spiketrains)))

p.end()
print(data_dir)
