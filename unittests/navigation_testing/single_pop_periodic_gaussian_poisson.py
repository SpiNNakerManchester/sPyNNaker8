# Standard library imports
import errno
import os
import random
import time
import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import utilities as util
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.space import Grid2D
from pyNN.utility.plotting import Figure, Panel
import spynnaker8 as p

"""
Grid cell model with periodic boundary constraints
Connectivity: distance-dependent 
Broad feedforward input: Poisson neuron
Velocity input: none
"""
p.setup(1)  # simulation timestep (ms)
runtime = 10  # ms

n_row = 128
n_col = 128
neuron_count = n_row * n_col

rng = NumpyRNG(seed=77364, parallel_safe=True)
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

# Parameters
self_connections = False  # allow self-connections in recurrent grid cell network
max_inh_synaptic_weight = 1.0  # synaptic weight for inhibitory connections
inh_synaptic_radius = 25  # inhibitory connection radius
centre_shift = 10  # number of neurons to shift centre of connectivity by
dc_input_rate = 100

# Grid cell (excitatory) population
# Grid cell neuron parameters
gc_neuron_params = {
    "v_thresh": -50.0,
    "v_reset": -65.0,
    "v_rest": -65.0,
    "i_offset": 0,
    "tau_m": 20,
    "tau_refrac": 1.0,
}
v_init = RandomDistribution('uniform', low=-65, high=-55, rng=rng)

# Network structure
neuron_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0, y0=0, z=0, fill_order='sequential')

# Populations
pop_dc_input = p.Population(neuron_count,
                            p.SpikeSourcePoisson(rate=dc_input_rate, start=0, duration=runtime),
                            structure=neuron_grid,
                            label="Poisson DC input cells")

pop_exc_gc = p.Population(neuron_count,
                          p.IF_curr_exp(**gc_neuron_params),
                          cellparams=None,
                          initial_values={'v': v_init},
                          structure=neuron_grid,
                          label="Excitatory grid cells")

# Connections
# DC Input pop to GC pop
proj_dc_input_gc = p.Projection(pop_dc_input, pop_exc_gc,
                                p.OneToOneConnector(),
                                synapse_type=p.StaticSynapse(weight=1.0, delay=1.0),
                                receptor_type='excitatory',
                                label="DC Input exc connections onto GC pop")

# GC pop inhibitory recurrent connections
inh_loop_connections = list()
for pre_syn in range(0, neuron_count):
    presyn_pos = (pop_exc_gc.positions[pre_syn])[:2]
    dir_pref = np.array(util.get_dir_pref(presyn_pos))

    # Shift centre of connectivity in appropriate direction
    shifted_centre = util.shift_centre_connectivity(presyn_pos, dir_pref, centre_shift, n_row, n_col)

    for post_syn in range(0, neuron_count):
        # If different neurons
        if pre_syn != post_syn or self_connections:
            post_syn_pos = (pop_exc_gc.positions[post_syn])[:2]
            euc_dist = util.get_neuron_distance_periodic(n_col, n_row, shifted_centre, post_syn_pos)

            # Establish connection
            if np.all(euc_dist <= inh_synaptic_radius):
                # Weight follows gaussian distribution. High inhibition to closer neighbours.
                weight = (1 - (euc_dist / inh_synaptic_radius)) * max_inh_synaptic_weight
                # Delay is between 1 and 5ms, based on distance
                singleConnection = (pre_syn, post_syn, weight, util.normalise_round(euc_dist, 1, 5))
                inh_loop_connections.append(singleConnection)

proj_gc_inhib = p.Projection(pop_exc_gc, pop_exc_gc,
                             # p.IndexBasedProbabilityConnector(
                             #     callback=progress_bar.set_level,
                             #     index_expression=,
                             #     allow_self_connections=is_auto_receptor,
                             #     rng=rng
                             # ),
                             p.FromListConnector(inh_loop_connections, ('weight', 'delay')),
                             p.StaticSynapse(),
                             receptor_type='inhibitory',
                             label="Recurrent GC inhibitory connections")

"""
RUN
"""
pop_exc_gc.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])
pop_dc_input.record(["spikes"])

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
f.write("Grid cell model")
f.write("\nruntime=" + str(runtime))
f.write("\nn_row=" + str(n_row))
f.write("\nn_col=" + str(n_col))
f.write("\norientation_pref_shift=" + str(centre_shift))
# f.write("\ninh_connections=" + str(inh_loop_connections))
f.write("\nsyn_radius=" + str(inh_synaptic_radius))
f.write("\npop_exc=" + str(pop_exc_gc.describe()))
f.close()

rand_neurons = random.sample(range(0, neuron_count), 4)
neuron_sample = p.PopulationView(pop_exc_gc, rand_neurons)
neuron_sample_dc = p.PopulationView(pop_dc_input, rand_neurons)

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(neuron_sample.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_inh')[0],
          ylabel="Inhibitory synaptic conduction (mV)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(neuron_sample.get_data().segments[0].filter(name='gsyn_exc')[0],
          ylabel="Excitatory synaptic conduction (mV)",
          xlabel="Time (ms)",
          data_labels=[neuron_sample.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(neuron_sample.get_data().segments[0].spiketrains,
          yticks=True, xticks=rand_neurons, markersize=0.2, xlim=(0, runtime)
          ),
)
plt.yticks(rand_neurons)
plt.savefig(data_dir + "sample_plot.eps", format='eps', bbox_inches='tight')
plt.show()

F = Figure(
    Panel(neuron_sample_dc.get_data().segments[0].spiketrains,
          data_labels=[neuron_sample.label], yticks=True, xticks=True, markersize=0.2, xlim=(0, runtime)
          ),
)
plt.yticks(rand_neurons)
plt.savefig(data_dir + "sample_plot_dc_input.eps", format='eps', bbox_inches='tight')
plt.show()

util.plot_gc_inh_connections(rand_neurons,
                             pop_exc_gc.positions,
                             max_inh_synaptic_weight,
                             inh_loop_connections,
                             n_col, n_row, data_dir)

mean_spike_count = pop_exc_gc.mean_spike_count(gather=True)
# max_firing_rate = util.compute_max_firing_rate(pop_exc_gc.get_data().segments[0].spiketrains, runtime)
# max_gsyn_exc = 0
# for item in pop_exc_gc.get_data().segments[0].filter(name='gsyn_exc')[0]:
#     m = float(max(item))
#     if m > max_gsyn_exc:
#         max_gsyn_exc = m

p.end()

# print("Max gsyn exc: " + str(max_gsyn_exc))
print("Mean spike count: " + str(mean_spike_count))
# print("Max firing rate: " + str(max_firing_rate))
print(data_dir)
