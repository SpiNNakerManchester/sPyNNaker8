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

spike_times = [1]# ,11,12,13,14,15,16,17, 18, 19,20]
spike_times_prob = [100, 110]# ,11,12,13,14,15,16,17, 18, 19,20]
# Spike source to send spike via plastic synapse

pop_src2 = p.Population(1000, p.SpikeSourcePoisson(rate=10), label="drive")

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")
# pop_src2 = p.Population(1, p.SpikeSourceArray,
#                         {'spike_times': spike_times_prob}, label="src_prob")

p.set_number_of_neurons_per_core(p.SpikeSourceArray, 1)



# Post-synapse population
# pop_exc = p.Population(1, p.extra_models.IF_curr_dual_exp(),  label="test")
pop_exc = p.Population(2, p.IF_curr_exp(),  label="test")

# Partition to single neuron per core
p.set_number_of_neurons_per_core(p.IF_curr_exp, 1)

# Create projections
synapse = p.Projection(
    pop_src2, pop_exc, p.FixedProbabilityConnector(0.000001),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

synapse2 = p.Projection(
    pop_src1, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=6, delay=1), receptor_type="excitatory")




# synapse2 = p.Projection(
#     pop_src1, pop_exc, p.FixedProbabilityConnector(0.01),
#     p.StaticSynapse(weight=0.6, delay=10), receptor_type="excitatory")

pop_src1.record('all')
pop_exc.record("all")
p.run(runtime)
weights = []
#
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


