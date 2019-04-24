import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1)
runtime = 1024

spike_times_exc = [10]# ,11,12,13,14,15,16,17, 18, 19,20]
spike_times_inh = [400]# ,11,12,13,14,15,16,17, 18, 19,20]

pop_src_exc = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times_exc}, label="src1")

pop_src_inh = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times_inh}, label="src1")

# Example Distributions
delay_dist = p.RandomDistribution(distribution='exponential', beta=[5.0])

default_params = {
    "v": 5.0,
    "v_rest": 0.0,
    "v_reset": 0.0,
    "i_offset": 0.25
    }

# Post-synapse population
pop_readout = p.Population(1, p.extra_models.SinusoidReadout(**default_params),
                           label="readout_pop")

# Create projections
synapse_exc = p.Projection(
    pop_src_exc, pop_readout, p.OneToOneConnector(),
    p.StaticSynapse(weight=1, delay=delay_dist), receptor_type="excitatory")
synapse_inh = p.Projection(
    pop_src_inh, pop_readout, p.OneToOneConnector(),
    p.StaticSynapse(weight=1, delay=delay_dist), receptor_type="inhibitory")

pop_src_exc.record('all')
pop_src_inh.record('all')
pop_readout.record("all")
p.run(runtime)

exc_pre_spikes = pop_src_exc.get_data('spikes')
inh_pre_spikes = pop_src_inh.get_data('spikes')
readout_data= pop_readout.get_data()

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
#     Panel(exc_pre_spikes.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
#     Panel(inh_pre_spikes.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(readout_data.segments[0].filter(name='v')[0],
          ylabel="Readout (Membrane potential (mV))",
          data_labels=[pop_readout.label], yticks=True, xlim=(0, runtime)),
    Panel(readout_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="Target",
          data_labels=[pop_readout.label], yticks=True, xlim=(0, runtime)),
    Panel(readout_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Error to target",
          data_labels=[pop_readout.label], yticks=True, xlim=(0, runtime)),
)
plt.show()
p.end()


