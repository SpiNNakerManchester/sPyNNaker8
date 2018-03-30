import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np

pre_rate = 100
nrn = 1
dt=1

p.setup(1)

simtime = 100

pop_src = p.Population(nrn, p.SpikeSourcePoisson(rate=pre_rate), label="src")
# pop_ex = p.Population(nrn, p.IF_curr_exp(),  label="test")
#
# proj2 = p.Projection(pop_src,  pop_ex,  p.OneToOneConnector(),
#                synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')

# pop_ex.record(['v',  'spikes'])
pop_src.record('spikes')

for i in range(simtime/dt):
        print i
        p.run(dt)

# v = pop_ex.get_data('v')
pre_spikes = pop_src.get_data('spikes')
# spikes = pop_ex.get_data('spikes')
plot_time = simtime
Figure(
    # raster plot of the presynaptic neuron spike times
     Panel(pre_spikes.segments[0].spiketrains,
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['pre-spikes']),
#     Panel(v.segments[0].filter(name='v')[0],
#           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, ylabel='V'),
#     Panel(spikes.segments[0].spiketrains,
#           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True,  data_labels=['post-spikes']),
#     title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))
plt.show()

p.end()
print "\n job done"