import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # set simulation timestep (ms)
runtime = 200


# Post-synapse population
neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -70,
    "i_offset": 0,
                 }

# pop_exc = p.Population(1, p.Izhikevich(**neuron_params),  label="LIF Neuron")

pop_exc = p.Population(1, p.extra_models.IzkCurrCombExp4E4I(**neuron_params),  label="LIF Neuron")


spike_times = [10, 15, 17, 19, 21]
# Spike source to send spike via synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")


# Create projection
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(0.6),
    p.StaticSynapse(weight=2, delay=1), receptor_type="excitatory3")

pop_src1.record('all')

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
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
#           ylabel="gsyn inhibitory (mV)",
#           data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    )

plt.show()
p.end()


