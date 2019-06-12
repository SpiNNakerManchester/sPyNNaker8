import spynnaker8 as p
import matplotlib.pyplot as plt
from pyNN.utility.plotting import Figure, Panel
from pyNN.space import Grid2D
from pyNN.random import RandomDistribution, NumpyRNG

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

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 0,  # DC input
    "i_vel_drive": 0,
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 0.1,
    "dir_pref": 0
}

rng = NumpyRNG(seed=41, parallel_safe=True)
v_init = RandomDistribution('uniform', (-70, -55), rng)
pop_exc = p.Population(1,
                       p.extra_models.GridCell(**neuron_params),
                       cellparams=None,
                       initial_values={'v': v_init},
                       structure=None,
                       label="Grid cells"
                       )

pop_exc.record("all")
pop_exc.describe(template='grid_cell_pop_default.txt', engine='default')
p.run(runtime)

exc_data = pop_exc.get_data()

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()
