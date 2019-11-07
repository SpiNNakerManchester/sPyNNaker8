from __future__ import print_function
import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep=1
p.setup(timestep) # simulation timestep (ms)
runtime = 1024
tau_err=20
l_rate=0.1
w_plastic=0.5

# # Post-synapse population
neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -70,
#     "v_rest": -65,
    "i_offset": 0.5, # DC input
    "v": 0
                 }

pop_exc = p.Population(3, # HARDCODE TO 3: One readout; one exc err, one inh err
                       p.extra_models.ReadoutPoissonNeuronNonSpike(
                            **neuron_params
                           ),  # Neuron model
                       label="Readout Neuron" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [[200, 600]]
pop_src1 = p.Population(1, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )


# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=l_rate, A_minus=l_rate),
    weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=1),
    weight=w_plastic,
    delay=timestep)


# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(),
    synapse_type=learning_rule, receptor_type="excitatory")

pop_src1.record('spikes')
pop_exc.record("all")

p.run(runtime)

pre_spikes = pop_src1.get_data('spikes')
test = pop_exc.spinnaker_get_data('spikes')
test_v = pop_exc.spinnaker_get_data('v')
# import numpy as np
# np.savetxt("~/test.csv", test_v, delimiter=", ")
exc_data = pop_exc.get_data()

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(pre_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
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
    annotations="Average firing freq: {}".format(
    len(exc_data.segments[0].spiketrains[0]))
    )

plt.show()
p.end()


print("job done")

