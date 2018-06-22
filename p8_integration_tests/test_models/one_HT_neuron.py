import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 0.1
p.setup(timestep) # set simulation timestep (ms)
runtime = 750

# Post-synapse population
neuron_params = {
        'v_init': -65,
        'g_Na': 0.2,
        'E_Na': 30.0,
        'g_K': 1.85,
        'E_K': -90.0,
        'tau_m': 16,
        't_spike': 2,
        'i_offset': 35,
        }

pop_exc = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")

spike_times = [10, 15, 17, 170, 190, 192, 200, 205, 400, 405, 410, 415, 420,
               425, 430, 435, 440, 721]
# Spike source to send spike via synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")


# Create projection
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(0.6),
    p.StaticSynapse(weight=100, delay=1), receptor_type="excitatory")

# pop_src1.record('all')

pop_exc.record("all")
p.run(runtime)
weights = []

# pre_spikes = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()


# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
#     Panel(pre_spikes_slow.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Threshold (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    )

plt.show()
p.end()


