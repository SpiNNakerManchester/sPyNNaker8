import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 1000

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0 # DC input
                 }

recurrent_pop_size = 1

pop_recurrent = p.Population(recurrent_pop_size, # number of neurons
                       p.IF_curr_exp(**neuron_params),  # Neuron model
                       label="recurrent" # identifier
                       )

# Spike source to send spike via synapse
spike_times = [[10, 15, 25], [1, 3]]
pop_input = p.Population(2, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="input" # identifier
                        )


# Instantiate BPTT SGD vertex
pop_bptt_sgd = p.Population(recurrent_pop_size,
                            p.BpttSgd(n_neurons=recurrent_pop_size),
                            label='instanced_bptt_sgd')

# # Create projection from source to LIF neuron
# synapse2 = p.Projection(
#     pop_input, pop_bptt_sgd, p.AllToAllConnector(),
#     p.StaticSynapse(weight=2, delay=1))

# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_input, pop_recurrent, p.AllToAllConnector(),
    p.StaticSynapse(weight=2, delay=1), receptor_type="excitatory")

pop_input.record('spikes')
pop_recurrent.record("all")

p.run(runtime)

pre_spikes = pop_input.get_data('spikes')
test = pop_recurrent.spinnaker_get_data('spikes')
test_v = pop_recurrent.spinnaker_get_data('v')

recurrent_data = pop_recurrent.get_data()

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(pre_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(recurrent_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_recurrent.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(recurrent_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_recurrent.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(recurrent_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)
          ),
    )


plt.show()
p.end()


