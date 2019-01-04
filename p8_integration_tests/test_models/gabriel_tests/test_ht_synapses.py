import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(0.1)
runtime = 1000

# Spike source to send spike via plastic synapse
AMPA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [10]}, label="src1")
NMDA_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [60]}, label="src1")
GABA_A_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [30]}, label="src1")
GABA_B_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [160]}, label="src1")


# Post-synapse population
pop_exc = p.Population(1, p.extra_models.HillTononi(),  label="test")

# Create projections
synapse_AMPA = p.Projection(
    AMPA_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="AMPA")
synapse_NMDA = p.Projection(
    NMDA_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.075, delay=1), receptor_type="NMDA")
synapse_GABA_A = p.Projection(
    GABA_A_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.33, delay=1), receptor_type="GABA_A")
synapse_GABA_B = p.Projection(
    GABA_B_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.0132, delay=1), receptor_type="GABA_B")

pop_exc.record("all")
p.run(runtime)
weights = []


runtime = runtime/0.1 # temporary scaling to account for new recording
weights.append(synapse_GABA_B.get('weight', 'list',
                                   with_address=False)[0])

exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
# p.end()


