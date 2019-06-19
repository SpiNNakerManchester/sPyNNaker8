import spynnaker8 as p
import matplotlib.pyplot as plt
from pyNN.utility.plotting import Figure, Panel
from pyNN.space import Grid2D
from pyNN.random import RandomDistribution, NumpyRNG
import utilities as util
import numpy as np


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

p.setup(1)  # simulation timestep (ms)
runtime = 200

grid_row = 8
grid_col = 8
p.set_number_of_neurons_per_core(p.IF_curr_exp, grid_row*grid_col)

is_auto_receptor = False

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 0.9,  # DC input
    "i_vel_drive": 0,
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1,
}

rng = NumpyRNG(seed=77364, parallel_safe=True)

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
view_exc = p.PopulationView(pop_exc, np.array([0,1,2,3]))

synaptic_weight = -0.6
synaptic_delay = RandomDistribution('uniform', low=0, high=5, rng=rng)
synaptic_radius = 4
orientation_pref_shift = 1

# Create recurrent connections
loopConnections = list()
for i in range(0, grid_row*grid_col):
    # print(str(pop_exc.positions[i]) + " Dir: " + str(util.get_dir_pref(pop_exc.positions[i])))
    for j in range(0, grid_row*grid_col):
        # If different neurons
        if (i != j or is_auto_receptor):
            i_pos = (pop_exc.positions[i])[:2]
            j_pos = (pop_exc.positions[j])[:2]
            diff_pos = np.subtract(j_pos, i_pos)
            dir_pref = np.array(util.get_dir_pref(i_pos))

            # # Wrap plane into torus
            # if((i_pos[0] == 0 and j_pos[0] == grid_row-1) or
            #         (i_pos[0] == grid_row-1 and j_pos[0] == 0)):
            #     diff_pos[0] = 1
            # if((i_pos[1] == 0 and j_pos[1] == grid_row-1) or
            #         (i_pos[1] == grid_row-1 and j_pos[1] == 0)):
            #     diff_pos[1] = 1

            if(np.all(abs(np.subtract(diff_pos, orientation_pref_shift * dir_pref)) <= synaptic_radius)):
                singleConnection = (i, j)
                loopConnections.append(singleConnection)

# space = p.Space(axes='xy', periodic_boundaries=((0, 100), (0, 100), None))
proj_exc = p.Projection(
    pop_exc, pop_exc, p.FromListConnector(loopConnections),
    p.StaticSynapse(weight=synaptic_weight, delay=synaptic_delay.next()),
    receptor_type='inhibitory',
    label="inhibitory connections")

pop_exc.record("all")
p.run(runtime)

exc_data = view_exc.get_data()
firing_rate = pop_exc.mean_spike_count(gather=True) * (1000/runtime)
print("Mean spike count=" + str(pop_exc.mean_spike_count(gather=True)))

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()

# print(pop_exc.describe(template='population_default.txt', engine='default'))
print(loopConnections)
print("Firing rate=" + str(firing_rate) + "Hz")
print("i_offset=" + str(neuron_params['i_offset']) + "nA")
print("tau_refrac=" + str(neuron_params['tau_refrac']) + "ms")
print("tau_m=" + str(neuron_params['tau_m']) + "ms")
