import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 200

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0, # DC input
    "i_vel": [1.0, 2.0, 3.0]
                 }

pop_exc = p.Population(3, # number of neurons
                       p.extra_models.GridCell(**neuron_params),  # Neuron model
                       label="Grid Cell" # identifier
                       )

pop_exc.record("all")

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
