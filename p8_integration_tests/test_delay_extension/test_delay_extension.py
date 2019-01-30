import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 1
p.setup(timestep) # simulation timestep (ms)
runtime = 200

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0 # DC input
                 }

pop_exc = p.Population(1, # number of neurons
                       p.IF_curr_exp(**neuron_params),  # Neuron model
                       label="LIF Neuron" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [[1, 2], [1], [1,12]]
pop_src1 = p.Population(3, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )



# Create projection from source to LIF neuron
delays=[1, 87, 144]
synapse = p.Projection(
    pop_src1, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.5, delay=delays), receptor_type="excitatory")

pop_src1.record('spikes')
pop_exc.record("all")

p.run(runtime)

pre_spikes = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()



# # Plot
# F = Figure(
#     # plot data for postsynaptic neuron
#     Panel(pre_spikes.segments[0].spiketrains,
#           yticks=True, markersize=2, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].filter(name='v')[0],
#           ylabel="Membrane potential (mV)",
#           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)
#           ),
#     Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
#           ylabel="gsyn excitatory (mV)",
#           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)
#           ),
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=2, xlim=(0, runtime)
#           ),
#     )



# F.fig.set_adjustable()
# F.fig.subplots_adjust(hspace=2)

gsyn_exc = exc_data.segments[0].filter(name='gsyn_exc')[0]
spikes = []
for i in range(len(gsyn_exc)):
    if gsyn_exc[i][0] > (0.45):
        spikes.append(i)

delays_plus_timestep = [d + timestep for d in delays]
print "SpiNNaker spikes: {}, Target spikes: {}".format(spikes, delays_plus_timestep)

p.end()
print "job done"

plt.show()