import spynnaker8 as p
from pyNN.random import RandomDistribution
import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import seaborn as sns


timestep = 1
runtime = 10000
initial_run = 100  # to negate any initial conditions

n_neurons = 400

frequencies = []


p.setup(timestep)

# test-neuron
pop_exc = p.Population(n_neurons,
                       p.IF_curr_exp(tau_m=30, cm=30,
                                     v_rest=0, v_reset=13.5, v_thresh=15,
                                     tau_syn_E=3, tau_syn_I=3, tau_refrac=3,
                                     i_offset=RandomDistribution("uniform", low=14.95, high=15.05)),
                                     #i_offset=RandomDistribution("uniform", low=14.625, high=15.375)),
                       label="test")

#pop_exc.initialize(v=13.5)

pop_exc.record("all")
p.run(initial_run + runtime)

exc_data = pop_exc.get_data()

# print "neuron firing frequency: {} Hz".format(
#      len(exc_data.segments[0].spiketrains[0]))

#frequencies.append(len(exc_data.segments[0].spiketrains[0]))

for train in exc_data.segments[0].spiketrains:
    frequencies.append(len(train)/10.)

# Plot
# Figure(
#     # plot data for postsynaptic neuron
#     Panel(exc_data.segments[0].filter(name='v')[0],
#           ylabel="Membrane potential (mV)",
#           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
# #     Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
# #           ylabel="gsyn excitatory (mA)",
# #           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
# #     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
# #           ylabel="gsyn inhibitory (mV)",
# #           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
# #     Panel(exc_data.segments[0].spiketrains,
# #           yticks=True, markersize=0.2, xlim=(0, runtime)),
#     # raster plot of the neuron spike times
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
#     annotations="neuron firing frequency: {} Hz".format(
#     len(exc_data.segments[0].spiketrains[0]))
# )
# plt.show()
# p.end()


plt.figure(1)
#plt.plot(exc_data.segments[0].spiketrains)
sns.distplot(frequencies, bins=20)
#plt.plot(currents, frequencies)
#plt.xlabel('offset current (A)')
#plt.ylabel('frequency (Hz)')
plt.show()

