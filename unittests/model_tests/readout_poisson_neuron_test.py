import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 1024

# # Post-synapse population
neuron_params = {
#     "v_thresh": -50,
#     "v_reset": -70,
#     "v_rest": -65,
    "i_offset": 0.5, # DC input
    "v": 0
                 }

pop_exc = p.Population(3, # HARDCODE TO 3: One readout; one exc err, one inh err
                       p.extra_models.ReadoutPoissonNeuron(
                            **neuron_params
                           ),  # Neuron model
                       label="LIF Neuron" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [[60, 70, 80, 90, 120, 125, 152], []]
pop_src1 = p.Population(2, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )

# Spike source to send spike via synapse
spike_times_2 = [[20, 40, 50, 80, 100, 105, 110, 120, 140, 150], []]
pop_src2 = p.Population(2, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times_2}, # source spike times
                        label="src2" # identifier
                        )

# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_src2, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=5.5, delay=1), receptor_type="excitatory")


# Create projection from source to LIF neuron
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=5.5, delay=1), receptor_type="excitatory")

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


print("job done")
