import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 1
p.setup(timestep)
runtime = 350
initial_run = 100  # to negate any initial conditions

# STDP parameters
STP_type = True
f_F = 0.5
P_baseline = 0.5
tau_P = 7
baseline_weight = 1

spike_times = [1, 6, 8, 11, 100]
spike_times = [initial_run + i for i in spike_times]

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
        timing_dependence=p.AbbotSTP(STP_type, f_F, P_baseline, tau_P),
        weight_dependence=p.MultiplicativeWeightDependence(
            ),
        weight=baseline_weight, delay=timestep)

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


