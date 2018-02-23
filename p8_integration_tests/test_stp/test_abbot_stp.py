import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1)
runtime = 1000
initial_run = 15  # to negate any initial conditions

# STDP parameters
a_plus = 0.01
a_minus = 0.01
tau_plus = 20
tau_minus = 20
plastic_delay = 3
initial_weight = 1
max_weight = 5
min_weight = 0

spike_times = [1, 6, 11]
# Spike source to send spike via plastic synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")


# Post-synapse population
pop_exc = p.Population(1, p.IF_curr_exp(),  label="test")

# Create projections
# synapse = p.Projection(
#     pop_src1, pop_exc, p.AllToAllConnector(),
#     p.StaticSynapse(weight=0.01, delay=1), receptor_type="excitatory")

syn_plas = p.STDPMechanism(
        timing_dependence=p.AbbotSTP(),
        weight_dependence=p.MultiplicativeWeightDependence(
            w_min=min_weight, w_max=max_weight),
        weight=initial_weight, delay=plastic_delay)

synapse = p.Projection(pop_src1, pop_exc,
                                       p.OneToOneConnector(),
                                       synapse_type=syn_plas)



pop_src1.record('all')
pop_exc.record("all")
p.run(initial_run + runtime)
weights = []

weights.append(synapse.get('weight', 'list',
                                   with_address=False)[0])

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
#     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
#           ylabel="gsyn inhibitory (mV)",
#           data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
p.end()


