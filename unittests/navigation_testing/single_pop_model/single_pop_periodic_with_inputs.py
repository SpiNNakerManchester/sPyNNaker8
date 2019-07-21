# Standard library imports
import cPickle as pickle
import time
import numpy as np
from neo.io import NixIO
import os
import errno

# Third party imports
import spynnaker8 as p

# Local application imports
import utilities as util
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.space import Grid2D, Line

"""
SETUP
"""
p.setup(1)  # simulation timestep (ms)
runtime = 2000  # ms

n_row = 50
n_col = 50
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

is_auto_receptor = False  # allow self-connections in recurrent grid cell network

rng = NumpyRNG(seed=77364, parallel_safe=True)
synaptic_weight = 0.6  # synaptic weight for inhibitory connections
synaptic_radius = 10  # inhibitory connection radius
orientation_pref_shift = 1  # number of neurons to shift centre of connectivity by

# Grid cell (excitatory) population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 0.8,
    "tau_m": 20,
    "tau_refrac": 1,
}

exc_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0, y0=0, z=0, fill_order='sequential')
# exc_space = p.Space(axes='xy', periodic_boundaries=((-n_col / 2, n_col / 2), (-n_row / 2, n_row / 2)))
v_init = RandomDistribution('uniform', low=-65, high=-55, rng=rng)
pop_exc = p.Population(n_row * n_col,
                       p.IF_curr_exp(**neuron_params),
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
    presyn_pos = (pop_exc.positions[pre_syn])
    dir_pref = np.array(util.get_dir_pref(presyn_pos))

    # Shift centre of connectivity in appropriate direction
    shifted_centre = util.shift_centre_connectivity(presyn_pos, dir_pref, orientation_pref_shift, n_row, n_col)
    for post_syn in range(0, n_row * n_col):
        # If different neurons
        if pre_syn != post_syn or is_auto_receptor:
            postsyn_pos = (pop_exc.positions[post_syn])
            dist = util.get_neuron_distance_periodic(n_col, n_row, shifted_centre, postsyn_pos)

            # Establish connection
            if np.all(dist <= synaptic_radius):
                single_connection = (pre_syn, post_syn, synaptic_weight, util.normalise(dist, 0, max(n_row, n_col)))
                loop_connections.append(single_connection)

# Create inhibitory connections
proj_exc = p.Projection(
    pop_exc, pop_exc, p.FromListConnector(loop_connections, ('weight', 'delay')),
    p.StaticSynapse(),
    receptor_type='inhibitory',
    label="Excitatory grid cells inhibitory connections")

# Input population encoding speed and head direction
# 0: N
# 1: E
# 2: W
# 3: S
# input_neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -65,
#     "v_rest": -65,
#     "i_offset": [0.8, 0.0, 0, 0],
#     "tau_m": 20,
#     "tau_refrac": 1,
# }
# input_structure = Line(dx=1.0, x0=0.0, y=0.0, z=0.0)
# input_loop_connections = list()
# pop_input = p.Population(4,
#                          p.IF_curr_exp(**input_neuron_params),
#                          structure=input_structure,
#                          label="Input head direction and speed cells")

input_structure = Line(dx=1.0, x0=0.0, y=0.0, z=0.0)
input_loop_connections = list()
pop_input = p.Population(4,
                         p.SpikeSourcePoisson(
                             rate=10.0, start=0.0, duration=runtime),
                         structure=input_structure,
                         label="Poisson input velocity cells")

# Connect input neuron to grid cells of appropriate direction
for i, neuron_pos in enumerate(pop_exc.positions):
    neuron_pref_dir = util.get_dir_pref(neuron_pos)
    if np.all(neuron_pref_dir == [0, 1]):
        single_connection = (0, i, 1.0, 1.0)
        index_north_cells.append(i)
    elif np.all(neuron_pref_dir == [0, -1]):
        single_connection = (3, i, 0.0, 1.0)
        index_south_cells.append(i)
    elif np.all(neuron_pref_dir == [1, 0]):
        single_connection = (1, i, 0.0, 1.0)
        index_east_cells.append(i)
    elif np.all(neuron_pref_dir == [-1, 0]):
        single_connection = (2, i, 0.0, 1.0)
        index_west_cells.append(i)
    input_loop_connections.append(single_connection)

view_exc_north = p.PopulationView(pop_exc, index_north_cells)
view_exc_east = p.PopulationView(pop_exc, index_east_cells)
view_exc_west = p.PopulationView(pop_exc, index_west_cells)
view_exc_south = p.PopulationView(pop_exc, index_south_cells)

proj_input = p.Projection(
    pop_input, pop_exc, p.FromListConnector(input_loop_connections, ('weight', 'delay')),
    receptor_type="excitatory",
    synapse_type=p.StaticSynapse(),
    label="Velocity input cells excitatory connections to appropriate grid cells"
)

# proj_dir_input = p.Projection(
#     pop_input, pop_exc, p.FromListConnector(input_loop_connections, ('weight', 'delay')),
#     p.StaticSynapse(),
#     receptor_type="excitatory",
#     label="Direction input cells excitatory connections to appropriate grid cells"
# )

"""
RUN
"""

pop_exc.record(["spikes"])
pop_input.record(["spikes"])
p.run(runtime)

"""
WRITE DATA
"""

# Write data to files
data_dir = "data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + "/"

# Create directory
try :
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
pickle.dump(pop_exc.get_data().segments[0].spiketrains,
            open(data_dir + "pop_exc_spiketrains.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_exc.label, open(data_dir + "pop_exc_label.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_exc.positions, open(data_dir + "pop_exc_positions.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(neuron_params, open(data_dir + "pop_exc_parameters.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

# Excitatory population (direction views)
pickle.dump(view_exc_north.get_data().segments[0].spiketrains, open(data_dir + "pop_exc_north_spike_train.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(view_exc_east.get_data().segments[0].spiketrains, open(data_dir + "pop_exc_east_spike_train.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(view_exc_west.get_data().segments[0].spiketrains, open(data_dir + "pop_exc_west_spike_train.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(view_exc_south.get_data().segments[0].spiketrains, open(data_dir + "pop_exc_south_spike_train.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

# Input population
pickle.dump(pop_input.get_data().segments[0].spiketrains, open(data_dir + "pop_input_spike_trains.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_input.get_data().segments[0].filter(name='v'), open(data_dir + "pop_input_v.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
pickle.dump(pop_input.label, open(data_dir + "pop_input_label.pkl", 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

f = open(data_dir + "params.txt", "w")
f.write("Single population grid cell model with velocity input")
f.write("\npop_exc=" + str(neuron_params))
f.write("\nruntime=" + str(runtime))
f.write("\nn_row=" + str(n_row))
f.write("\nn_col=" + str(n_col))
f.write("\nsyn_weight=" + str(synaptic_weight))
f.write("\nsyn_radius=" + str(synaptic_radius))
f.write("\norientation_pref_shift=" + str(orientation_pref_shift) + "\n")
f.write("pop_input=" + str(pop_input.describe()))
f.close()

p.end()
util.check_connection_dir_prefs([2, 94, 494, 600], pop_exc.positions, loop_connections)
print(data_dir)

