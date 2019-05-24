import spynnaker8 as p
import matplotlib.pyplot as plt
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
from pyNN.space import Grid2D
from pyNN.random import RandomDistribution, NumpyRNG

'''
Model Parameters
cell_rows = 132
cell_cols = 112
timestep = 1
rest_pot = -65
reset_pot = -67
thres_pot = -63
membrane_time_constant = 10
membrane_resistance = 10
refractory_period = 5
input_curr = 2.4
vel_curr = 0.175
orientation_pref_shift = 2
syn_weight = -0.6
syn_delay = 5*rand()
'''

p.setup(1) # simulation timestep (ms)
runtime = 200

# Post-synapse population
neuron_params = {
    "v_thresh": -63,
    "v_reset": -67,
    "v_rest": -65,
    "i_offset": 2.4, # DC input
    "i_vel": 0.175,
    "tau_m": 10, # membrane time constant
    "tau_refrac": 5,
                 }

pop_grid = Grid2D(aspect_ratio=1.0, dx=1.0, dy=1.0, x0=0.0, y0=0.0, z=0, fill_order='sequential')
v_init = RandomDistribution('uniform', (-70, -60))
pop_exc = p.Population(4,
                       p.extra_models.GridCell(**neuron_params),
                       cellparams=None,
                       initial_values={'v': v_init},
                       structure=pop_grid,
                       label="Grid cells"
                       )

print(pop_exc.positions)
pop_exc.record("all")
# pop_exc.describe(template='grid_cell_pop_default.txt', engine='default')

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
