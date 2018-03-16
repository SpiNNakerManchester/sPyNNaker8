import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
from pyNN.random import RandomDistribution
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

p.setup(1)

inp_nrn = 2000
inh_nrn = 1000
inp_inh_conn_prob = 8.0/inh_nrn

w0 = 0.51
w_mult=0.1   # this parameters scales all weight variables, actual w_max = w_mult; should be 0.1-0.125 or smaller to avoid distortions in results
a_plus = 0.11
a_minus = 0.11
w_min = 0.0
w_max = 1.0
w_drift = .0035
th_w = 0.50
V_th = -56.0
Ca_th_l = 3.0
Ca_th_h1 = 4.0
Ca_th_h2 = 13.0



#w_mult = w_mult/inp_nrn
#simtime=300

#simtime = 1000
# p.set_number_of_neurons_per_core(p.IF_curr_exp, 50)
# p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 50)
# p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpCa2Concentration, 100)
# p.extra_models.IFCurrExpCa2Concentration.set_max_atoms_per_core(100)

pop_src = p.Population(inp_nrn, p.SpikeSourcePoisson(rate=10), label="src")
#pop_inp = p.Population(inp_nrn, p.IF_curr_exp(), label="inp")
pop_teacher = p.Population(1, p.SpikeSourcePoisson(rate=50), label="teacher")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,   'v_reset':-65}
#pop_inh = p.Population(inh_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="inhibitory")
pop_inh = p.Population(inh_nrn, p.IF_curr_exp(), label="inhibitory")
pop_ex = p.Population(1, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")
#pop_ex = p.Population(1, p.IF_curr_exp(), label="test")

rates = [2]*inp_nrn
for i in range(100):
    rates[i]=50
pop_src.set(rate=rates)

weights = [1]*inp_nrn
for i in range(1000):
     rates[i+50]=0.0*w_mult
rd = RandomDistribution('uniform', (0, w_mult))

syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(A_plus = a_plus*w_max*w_mult, A_minus = a_minus*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
        weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=rd, delay=1.0)

#syn = p.StaticSynapse(weight=1.0, delay=1.0)

proj = p.Projection(
    pop_src,
    pop_ex,
    p.AllToAllConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

proj_inp_inh = p.Projection(pop_src,  pop_inh,  p.FixedProbabilityConnector(inp_inh_conn_prob),
               synapse_type=p.StaticSynapse(weight=1.0),  receptor_type='excitatory')
proj_inh_ex = p.Projection(pop_inh,  pop_ex,  p.AllToAllConnector(),
               synapse_type=p.StaticSynapse(weight=w_mult),  receptor_type='inhibitory')
proj_teach_ex = p.Projection(pop_teacher,  pop_ex,  p.AllToAllConnector(),
               synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')



pop_ex.record(['v',  'spikes'])
pop_src.record('spikes')
pop_inh.record('spikes')

wgts=[]
if to_plot_wgts:
    for i in range(simtime):
        print i
        p.run(1)
        wgts.append( proj.get('weight', format='list', with_address=False)[0])
#        wgts.append( proj.get('weight', format='list', with_address=False)[0])
else:
        p.run(simtime)

#p.run(50)

v = pop_ex.get_data('v')
#curr = pop_ex.get_data('gsyn_exc')
pre_spikes = pop_src.get_data('spikes')
inh_spikes = pop_inh.get_data('spikes')
spikes = pop_ex.get_data('spikes')

avg_pre_rate=0.0;
avg_inh_rate=0.0;
for i in range(len(pre_spikes.segments[0].spiketrains)):
    avg_pre_rate+=pre_spikes.segments[0].spiketrains[i].shape[0]
for i in range(len(inh_spikes.segments[0].spiketrains)):
    avg_inh_rate+=inh_spikes.segments[0].spiketrains[i].shape[0]
avg_pre_rate = avg_pre_rate / len(pre_spikes.segments[0].spiketrains)
avg_inh_rate = avg_inh_rate / len(inh_spikes.segments[0].spiketrains)

print "pre", avg_pre_rate
print "inh", avg_inh_rate
print spikes.segments[0].spiketrains[0].shape

#print v.segments[0].filter(name='v')[0]
#print pre_spikes.segments[0].spiketrains
#print spikes.segments[0].spiketrains

plot_time = simtime
if to_plot_wgts:
    plot_wgt = DataTable(range(plot_time), wgts)

    Figure(
    # raster plot of the presynaptic neuron spike times
     Panel(pre_spikes.segments[0].spiketrains,
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['pre-spikes']),
 #   Panel(plot_wgt,
 #         yticks=True, xlim=(0, plot_time), xticks=True, ylabel='weight'),
    Panel(v.segments[0].filter(name='v')[0],
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, ylabel='V'),
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True,  data_labels=['post-spikes']),
    title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))
else:
    Figure(
    # raster plot of the presynaptic neuron spike times
     Panel(pre_spikes.segments[0].spiketrains[0:20],
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['pre-spikes']),
     Panel(inh_spikes.segments[0].spiketrains[0:10],
           yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, data_labels=['inhibitory spikes']),
    Panel(v.segments[0].filter(name='v')[0],
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True, ylabel='V'),
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.5, xlim=(0, plot_time), xticks=True,  data_labels=['post-spikes']),
    title="fusi spikes",
    annotations="Simulated with {}".format(p.name()))

#spike train is not written to the file???
io = PyNNTextIO(filename="data/data.txt")
pop_ex.write_data(io)
io = AsciiSpikeTrainIO(filename="data/pre_spikes.txt")
pop_src.write_data(io)
# io = AsciiSpikeTrainIO(filename="data/pre_spikes_static.txt")
# pop_src2.write_data(io)
io = AsciiSpikeTrainIO(filename="data/post_spikes.txt")
pop_ex.write_data(io)
p.end()
plt.show()
print "\n job done"