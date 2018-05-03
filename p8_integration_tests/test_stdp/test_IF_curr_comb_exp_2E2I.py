import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1)
runtime = 200
initial_run = 15  # to negate any initial conditions

# STDP parameters
a_plus = 0.01
a_minus = 0.01
tau_plus = 20
tau_minus = 20
plastic_delay = 3
initial_weight = 2.5
max_weight = 5
min_weight = 0

spike_times = [10]# ,11,12,13,14,15,16,17, 18, 19,20]
spike_times2 = [60]# ,11,12,13,14,15,16,17, 18, 19,20]
# Spike source to send spike via plastic synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")
pop_src2 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times2}, label="src2")


# Post-synapse population
pop_exc = p.Population(1, p.extra_models.IFCurrCombExp2E2I(),  label="test")


# print "weight precision: {}".format(p.get_weight_precision(p.IF_curr_exp))


# Create projections
synapse_exc = p.Projection(
    pop_src1, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.2, delay=1), receptor_type="excitatory")

# Create projections
synapse_exc2 = p.Projection(
    pop_src1, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.4, delay=15), receptor_type="excitatory2")

# Create projections
synapse_inh = p.Projection(
    pop_src2, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.6, delay=1), receptor_type="inhibitory")

# Create projections
synapse_inh2 = p.Projection(
    pop_src2, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.8, delay=15), receptor_type="inhibitory2")

pop_src1.record('all')
pop_exc.record("all")
p.run(runtime)
weights = []

# weights.append(synapse.get('weight', 'list',
#                                    with_address=False)[0])

pre_spikes_slow = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(pre_spikes_slow.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
        data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
p.end()


