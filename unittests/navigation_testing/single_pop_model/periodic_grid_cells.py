# Standard library imports
import matplotlib.pyplot as plt
import numpy as np

# Third party imports
import spynnaker8 as p
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.space import Grid2D
from pyNN.utility.plotting import Figure, Panel
from pyNN.standardmodels.electrodes import DCSource

# Local application imports
# from ..tools import utilities as util
# from ..agent_simulations import straight_walk as sim_straight_walk
import utilities as util
import straight_walk as sim_straight_walk

'''
Paper Model Parameters
cell_rows = 132
cell_cols = 112
timestep = 1
rest_pot = -65mV
reset_pot = -67mV
thres_pot = -63mV
membrane_time_constant = 10ms
membrane_resistance = 10 ohm
refractory_period = 5ms
input_curr = 2.4mA
vel_curr = 0.175mA
orientation_pref_shift = 2
syn_weight = -0.6mV
syn_delay = 5*rand()
'''

DEBUG = True

p.setup(1)  # simulation timestep (ms)
runtime = 1000  # ms

grid_row = 10
grid_col = 10
p.set_number_of_neurons_per_core(p.IF_curr_exp, 255)

is_auto_receptor = False

synaptic_weight = 0.6
# synaptic_delay = RandomDistribution('uniform', low=0, high=1, rng=rng)
synaptic_radius = 10
orientation_pref_shift = 1

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 0.8,  # DC input
    "i_vel_drive": 0,
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1,
}

rng = NumpyRNG(seed=77364, parallel_safe=True)

# Define excitatory population
pop_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0, y0=0, z=0, fill_order='sequential')
v_init = RandomDistribution('uniform', low=-65, high=-50, rng=rng)
pop_exc = p.Population(grid_row * grid_col,
                       p.extra_models.GridCell(**neuron_params),
                       cellparams=None,
                       initial_values={'v': v_init},
                       structure=pop_grid,
                       label="Grid cells"
                       )

# Create view
view_exc = p.PopulationView(pop_exc, np.array([0, 1, grid_col, grid_col+1]))

# Create recurrent connections
loopConnections = list()
for i in range(0, grid_row*grid_col):
    for j in range(0, grid_row*grid_col):
        # If different neurons
        if (i != j or is_auto_receptor):
            postsyn_pos = (pop_exc.positions[i])[:2]
            presyn_pos = (pop_exc.positions[j])[:2]
            euc_dist = util.get_neuron_distance_periodic(grid_col, grid_row, postsyn_pos, presyn_pos)
            dir_pref = np.array(util.get_dir_pref(presyn_pos))

            # Establish connection
            if(np.all(abs(euc_dist - (orientation_pref_shift * dir_pref) <= synaptic_radius))):
                singleConnection = (j, i, synaptic_weight, euc_dist)
                loopConnections.append(singleConnection)

# Create inhibitory connections
proj_exc = p.Projection(
    pop_exc, pop_exc, p.FromListConnector(loopConnections),
    p.StaticSynapse(),
    receptor_type='inhibitory',
    label="inhibitory connections")

# Stimulate direction
dir_to_stimulate = [0, 1]
dir_neurons = list()
for i, neuron_pos in enumerate(pop_exc.positions):
    if util.get_dir_pref(neuron_pos[:2]) == dir_to_stimulate:
        dir_neurons.append(i)

dir_view = p.PopulationView(pop_exc, dir_neurons)
dir_view.set(i_offset=0.8)

pop_exc.record("all")
p.run(runtime)

# Simulate agent movement
dir = [-1, 0]
agent_straight_walk = sim_straight_walk.StraightWalk(0.5, dir)

run_step = 100
# for i in range(0, runtime, run_step):
#     speed, head_dir = agent_straight_walk.get_velocity()
#     if DEBUG:
#         print("[DEBUG] Agent speed=" + str(speed)+ "m/s")
#         print("[DEBUG] Agent head direction=" + str(head_dir))
#     p.run(run_step)

    # Plot firing rate across manifold
    # util.plot_population_firing_rate(pop_exc.get_data().segments[0].spiketrains, pop_exc.positions, (i + 1) * run_step,
    #                                  grid_row, grid_col)

# Get trajectory
# trajectory = agent_straight_walk.get_positions(runtime)
# if DEBUG:
#     print("[DEBUG] Agent trajectory: " + str(trajectory))

exc_data_pop = pop_exc.get_data()
exc_data_view = view_exc.get_data()
firing_rate = pop_exc.mean_spike_count(gather=True) * (1000/runtime)
print("Mean spike count=" + str(pop_exc.mean_spike_count(gather=True)))

# Plot activity
spike_trains = exc_data_view.segments[0].spiketrains

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data_view.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data_view.segments[0].filter(name='gsyn_exc')[0],
          ylabel="Excitatory synaptic conduction (uS)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data_view.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Inhibitory synaptic conduction (uS)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(spike_trains,
          yticks=True, xticks=True, xlabel="Time (ms)", markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()

# util.plot_trajectory_infinite_1d(trajectory, dir, runtime, False)
util.plot_population_firing_rate(exc_data_pop.segments[0].spiketrains,
                                 pop_exc.positions, runtime, grid_row, grid_col, False)
util.plot_population_membrane_potential_activity(exc_data_pop.segments[0].filter(name='v')[0], pop_exc.positions,
                                                 [runtime], -65, -50, grid_row, grid_col, False)
# util.plot_population_spike_activity(grid_row, grid_col, spike_trains, pop_exc.positions, [381, 400])


# print(pop_exc.describe(template='population_default.txt', engine='default'))
if DEBUG:
    print(util.get_neuron_connections(0, loopConnections))
    print("Firing rate=" + str(firing_rate) + "Hz")
    print("i_offset=" + str(neuron_params['i_offset']) + "nA")
    print("tau_refrac=" + str(neuron_params['tau_refrac']) + "ms")
    print("tau_m=" + str(neuron_params['tau_m']) + "ms")