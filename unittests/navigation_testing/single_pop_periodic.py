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

"""
SETUP
"""
p.setup(1)  # simulation timestep (ms)
runtime = 20000  # ms

n_row = 128
n_col = 128
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

is_auto_receptor = True  # allow self-connections in recurrent grid cell network

rng = NumpyRNG(seed=77364, parallel_safe=True)
synaptic_weight = 0.05  # synaptic weight for inhibitory connections
synaptic_radius = 10  # inhibitory connection radius
orientation_pref_shift = 1  # number of neurons to shift centre of connectivity by

# Grid cell (excitatory) population
neuron_params = {
    "v_thresh": -50.0,
    "v_reset": -65.0,
    "v_rest": -65.0,
    "i_offset": 0.76,  # DC input
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1.0,
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

# Create recurrent inhibitory connections
loop_connections = list()
for pre_syn in range(0, n_row * n_col):
    presyn_pos = (pop_exc.positions[pre_syn])[:2]
    dir_pref = np.array(util.get_dir_pref(presyn_pos))

    # Shift centre of connectivity in appropriate direction
    shifted_centre = util.shift_centre_connectivity(presyn_pos, dir_pref, orientation_pref_shift, n_row, n_col)
    for post_syn in range(0, n_row * n_col):
        # If different neurons
        if pre_syn != post_syn or is_auto_receptor:
            postsyn_pos = (pop_exc.positions[post_syn])[:2]
            dist = util.get_neuron_distance_periodic(n_col, n_row, shifted_centre, postsyn_pos)

            # Establish connection
            if np.all(dist <= synaptic_radius):
                singleConnection = (pre_syn, post_syn, synaptic_weight, util.normalise(dist, 0, max(n_row, n_col)))
                # singleConnection = (pre_syn, post_syn, synaptic_weight, 1.0)
                loop_connections.append(singleConnection)

# Create inhibitory connections
proj_exc = p.Projection(
    pop_exc, pop_exc, p.FromListConnector(loop_connections, ('weight', 'delay')),
    p.StaticSynapse(),
    receptor_type='inhibitory',
    label="Excitatory grid cells inhibitory connections")

"""
RUN
"""
pop_exc.record(['v', 'gsyn_inh', 'spikes'])
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

rand_neurons = random.sample(range(0, n_col*n_row), 4)
neuron_sample = p.PopulationView(pop_exc, rand_neurons)

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_inh')[0],
          ylabel="inhibitory synaptic conduction (uS)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(neuron_sample.get_data().segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)
plt.yticks(rand_neurons)
plt.savefig(data_dir + "sample_plot.eps", format='eps', bbox_inches='tight')
plt.show()

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

f = open(data_dir + "params.txt", "w")
f.write("Single population grid cell (periodic) model")
f.write("\nruntime=" + str(runtime))
f.write("\nn_row=" + str(n_row))
f.write("\nn_col=" + str(n_col))
f.write("\nsyn_weight=" + str(synaptic_weight))
f.write("\nsyn_radius=" + str(synaptic_radius))
f.write("\norientation_pref_shift=" + str(orientation_pref_shift))
f.write("\npop_exc=" + str(pop_exc.describe()))
f.close()

# util.plot_connections([14232, 15000, 12854, 812], pop_exc.positions, loop_connections, n_col, n_row, data_dir)
# util.plot_neurons(pop_exc.positions, data_dir)
print("Mean spike count: " + str(pop_exc.mean_spike_count(gather=True)))
print("Max firing rate: " + str(util.compute_max_firing_rate(pop_exc.get_data().segments[0].spiketrains, runtime)))
p.end()
print(data_dir)
