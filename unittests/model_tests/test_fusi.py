import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from matplotlib.pyplot import legend
from idna.core import _alabel_prefix

to_plot_wgts = True
#to_plot_wgts = False

p.setup(1)

simtime = 100

# mysource = [10*range(1, 5)]
#mysource = [20,21, 40] #,4, 10,14]
mysource = [5,8,11, 14, 20, 23, 26, 40, 43] #,4, 10,14]
pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': mysource}, label="src")
cell_params = {"i_offset":0, "v_reset":-65, "tau_ca2":60, "i_alpha":1.0}
pop_ex = p.Population(1, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")



syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(A_plus = 1.0, A_minus = 1.0, th_v_mem=-56, th_ca_up_l = 3.0, th_ca_up_h = 13.0, th_ca_dn_l = 3.0, th_ca_dn_h = 4.0),
        weight_dependence = p.WeightDependenceFusi(w_min=0.0, w_max=10.0, w_drift=.035, th_w=5.0), weight=5.0, delay=1.0)

proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

pop_ex.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])
pop_src.record('spikes')

wgts=[]
if to_plot_wgts:
    for i in range(50):
        p.run(1)
        wgts.append( proj.get('weight', format='list', with_address=False)[0])
else:
        p.run(50)

#p.run(50)

v = pop_ex.get_data('v')
curr = pop_ex.get_data('gsyn_exc')
spikes = pop_ex.get_data('spikes')
pre_spikes = pop_src.get_data('spikes')

print v.segments[0].filter(name='v')[0]

plot_time = 50
if to_plot_wgts:
    plot_wgt = DataTable(range(plot_time), wgts)

    Figure(
    # raster plot of the presynaptic neuron spike times
     Panel(pre_spikes.segments[0].spiketrains,
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['pre-spikes']),
    Panel(plot_wgt,
          yticks=True, xlim=(0, plot_time), xticks=True, ylabel='weight'),
    Panel(v.segments[0].filter(name='v')[0],
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, ylabel='V'),
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True,  data_labels=['post-spikes']),
    title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))
else:
    Figure(
    # raster plot of the presynaptic neuron spike times
     Panel(pre_spikes.segments[0].spiketrains,
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['pre-spikes']),
    Panel(v.segments[0].filter(name='v')[0],
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, ylabel='V'),
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True,  data_labels=['post-spikes']),
    title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))
plt.show()


p.end()
print "\n job done"