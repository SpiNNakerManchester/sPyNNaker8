import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
p.setup(1)

simtime = 1000

# mysource = [10*range(1, 5)]
mysource = [2,4, 10,14]
pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': mysource}, label="src")
cell_params = {"i_offset":0, "v_reset":-70}
pop_ex = p.Population(1, p.IF_curr_exp, cell_params, label="test")

syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(A_plus = 0.5, A_minus = 0.4, th_v_mem=-60),
        weight_dependence = p.WeightDependenceFusi(w_min=1.0, w_max=5.0), weight=2.5, delay=1.0)

proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

pop_ex.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])
#pop_src.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])

p.run(simtime)

v = pop_ex.get_data('v')
curr = pop_ex.get_data('gsyn_exc')
spikes = pop_ex.get_data('spikes')
#pre_spikes = pop_src.get_data('spikes')
print v.segments[0].filter(name='v')[0]
import numpy
Figure(
    # raster plot of the presynaptic neuron spike times
#     Panel(numpy.array(mysource),
#           yticks=True, markersize=0.5, xlim=(0, 100), xticks=True),
    Panel(v.segments[0].filter(name='v')[0],
          yticks=True, markersize=0.5, xlim=(0, 50), xticks=True),
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.5, xlim=(0, 50), xticks=True),
    title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))
plt.show()


p.end()
print "\n job done"