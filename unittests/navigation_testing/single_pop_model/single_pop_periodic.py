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
runtime = 1000  # ms

n_row = 10
n_col = 10
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

is_auto_receptor = False  # allow self-connections in recurrent grid cell network

rng = NumpyRNG(seed=77364, parallel_safe=True)
synaptic_weight = 0.6  # synaptic weight for inhibitory connections
synaptic_radius = 1  # inhibitory connection radius
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

# Create view
# view_exc = p.PopulationView(pop_exc, np.array([0, 1, n_col, n_col + 1]))

# Create recurrent inhibitory connections
loopConnections = list()
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
                singleConnection = (pre_syn, post_syn, synaptic_weight, util.normalise(dist, 0, max(n_row, n_col)))
                loopConnections.append(singleConnection)

# Create inhibitory connections
proj_exc = p.Projection(
    pop_exc, pop_exc, p.FromListConnector(loopConnections, ('weight', 'delay')),
    p.StaticSynapse(),
    receptor_type='inhibitory',
    label="Excitatory grid cells inhibitory connections")

"""
RUN
"""
pop_exc.record("all")
p.run(runtime)

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
with open(data_dir + "pop_exc_data.pkl", 'wb') as f:
    f.write(pickle.dumps(pop_exc))
with open(data_dir + "pop_exc_parameters.pkl", 'wb') as f:
    f.write(pickle.dumps(neuron_params))

print(data_dir)

p.end()
