import spynnaker8 as p
import matplotlib.pyplot as plt
from pyNN.utility.plotting import Figure, Panel
from pyNN.space import Grid2D
from pyNN.random import RandomDistribution, NumpyRNG
import utilities as util

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
grid_row = 2
grid_col = 2
p.set_number_of_neurons_per_core(p.IF_curr_exp, grid_row*grid_col)

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 1,  # DC input
    "i_vel_drive": 0,
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 0.1,
}

rng = NumpyRNG(seed=41, parallel_safe=True)

synaptic_weight = -0.6
synaptic_delay = RandomDistribution('uniform', (5, 6), rng)
synaptic_radius = 1

pop_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0, y0=0, z=0, fill_order='sequential')
v_init = RandomDistribution('uniform', (-70, -55), rng)
pop_exc = p.Population(grid_row * grid_col,
                       p.extra_models.GridCell(**neuron_params),
                       cellparams=None,
                       initial_values={'v': v_init},
                       structure=pop_grid,
                       label="Grid cells"
                       )

# Initialise neuron directional preferences
# pop_exc.set(dir_pref=lambda i: util.init_dir_pref(pop_exc.positions[i]))

pop_exc.record("all")
print(pop_exc.describe(template='population_default.txt', engine='default'))

p.run(runtime)
exc_data = pop_exc.get_data()
firing_rate = len(exc_data.segments[0].spiketrains[0]) * (1000/runtime)

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

print("Firing rate=" + str(firing_rate) + "Hz")
print("i_offset=" + str(neuron_params['i_offset']) + "nA")
print("tau_refrac=" + str(neuron_params['tau_refrac']) + "ms")
print("tau_m=" + str(neuron_params['tau_m']) + "ms")
