import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 2000

# # Post-synapse population
neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -70,
#     "v_rest": -65,
    "i_offset": 0.0, # DC input
    "v": 75.0
                 }

pop_exc = p.Population(1, # number of neurons
                       p.extra_models.PoissonNeuron(
                            **neuron_params
                           ),  # Neuron model
                       label="LIF Neuron" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [[510, 515, 525, 904,], [1, 3, 940, 100, 1027, 1050, 1075, 1090, 1110]]
pop_src1 = p.Population(2, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )

# Spike source to send spike via synapse
spike_times_2 = [[500, 505, 510], [101, 130]]
pop_src2 = p.Population(2, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times_2}, # source spike times
                        label="src2" # identifier
                        )

# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_src2, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=10, delay=1), receptor_type="excitatory")


# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_src1, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=10, delay=1), receptor_type="excitatory")

pop_src1.record('spikes')
pop_exc.record("all")

# pop_exc.set(i_offset= 0)
# p.run(runtime/4)
# pop_exc.set(i_offset= 2)
# p.run(runtime/4)
# pop_exc.set(i_offset= 5)
# p.run(runtime/4)
# pop_exc.set(i_offset= 0.25)
# p.run(runtime/4)
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


print "job done"

