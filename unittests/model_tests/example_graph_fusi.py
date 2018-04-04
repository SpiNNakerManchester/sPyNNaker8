import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from matplotlib.pyplot import legend
from idna.core import _alabel_prefix

from neo.io import PyNNNumpyIO
from neo.io import AsciiSpikeTrainIO
from neo.io import PyNNTextIO
from example_graph_params import *


to_plot_wgts = True
to_plot_wgts = False

dr_r = 100
pre_rate = 50
nrn = 1
dt=20
# w_mult = w_mult/4

p.setup(1)

simtime = 1000


pop_src = p.Population(nrn, p.SpikeSourcePoisson(rate=pre_rate), label="src")
pop_src2 = p.Population(nrn, p.SpikeSourcePoisson(rate=dr_r), label="drive")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}
pop_ex = p.Population(nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")



syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(A_plus = 0.15*w_max*w_mult, A_minus = 0.15*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
        weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=w0*w_mult, delay=1.0)

#syn = p.StaticSynapse(weight=1.0, delay=1.0)

proj = p.Projection(
    pop_src,
    pop_ex,
    p.OneToOneConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

proj2 = p.Projection(pop_src2,  pop_ex,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')
# proj2 = p.Projection(
#     pop_src2,
#     pop_ex,
#     p.OneToOneConnector(),
#     syn,
#     receptor_type='excitatory'
#     )

pop_ex.record(['v',  'spikes'])
pop_src.record('spikes')
pop_src2.record('spikes')

wgts=np.zeros((simtime/dt, nrn))
if to_plot_wgts:
    for i in range(simtime/dt):
        print i
        p.run(dt)
        wgts[ i, :] = proj.get('weight', format='list', with_address=False)
        #wgts.append( proj.get('weight', format='list', with_address=False))
        #print proj.get('weight', format='list', with_address=False)
        print wgts
#        wgts.append( proj.get('weight', format='list', with_address=False)[0])
else:
        p.run(simtime)

#p.run(50)

v = pop_ex.get_data('v')
#curr = pop_ex.get_data('gsyn_exc')
pre_spikes = pop_src.get_data('spikes')
pre_spikes_static = pop_src2.get_data('spikes')
spikes = pop_ex.get_data('spikes')

#print v.segments[0].filter(name='v')[0]
#print pre_spikes.segments[0].spiketrains
#print spikes.segments[0].spiketrains
print type(pre_spikes.segments[0].spiketrains)
print len(range(0, simtime, dt))
wgts.shape
plot_time = simtime
if to_plot_wgts:
    plot_wgt = DataTable(range(0, plot_time, dt), wgts[:,nrn-1])
    print plot_wgt

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

#spike train is not written to the file???
io = PyNNTextIO(filename="data/data.txt")
pop_ex.write_data(io)
io = AsciiSpikeTrainIO(filename="data/pre_spikes.txt")
pop_src.write_data(io)
io = AsciiSpikeTrainIO(filename="data/pre_spikes_static.txt")
pop_src2.write_data(io)
io = AsciiSpikeTrainIO(filename="data/post_spikes.txt")
pop_ex.write_data(io)
p.end()
print "\n job done"