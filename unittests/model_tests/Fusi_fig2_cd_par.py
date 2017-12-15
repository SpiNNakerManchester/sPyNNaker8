import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from matplotlib.pyplot import legend
from idna.core import _alabel_prefix

import matplotlib.pyplot as plt

from neo.io import PyNNNumpyIO
from neo.io import AsciiSpikeTrainIO
from neo.io import PyNNTextIO
from example_graph_params import *
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

to_plot_wgts = True
to_plot_wgts = False

p.setup(1)

simtime = 300
n_runs = 1
w0 = 0.0
pre_rate = 50
drive_rates = np.arange(50, 60, 10) # driving source rates
n_rates = drive_rates.size
max_out_rate = 200
output_file = "data/fig2_"+timestr
output_ext = ".txt"

n_trans = np.zeros(max_out_rate+1) # number of weight transitions for each spiking rate of the output neuron for 0 to 200
n_tot = np.zeros(max_out_rate+1) # number of sims ran for each spiking rate of the output neuron (needed to calculate transition probability)

n_nrn = 3  # total number of neurons in each run

pop_src = p.Population(n_nrn, p.SpikeSourcePoisson(rate=pre_rate), label="src")
pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=100), label="drive")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.5,  'tau_m': 50.0, 'v_reset':-65}
pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")



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

pop_ex.record(['spikes'])
pop_src.record('spikes')
pop_src2.record('spikes')
nseg = 0
save_train = []
for r in range(n_runs):
    for dr_r in drive_rates:
        pop_src2.set(rate=dr_r) # this has to happen before every run because of the poisson souce bug
        pop_src.set(rate=pre_rate) # this has to happen before every run because of the poisson souce bug
        p.run(simtime)
        new_rates = np.zeros(n_nrn, dtype=int)
        trains = pop_ex.get_data('spikes').segments[nseg].spiketrains
        for n in range(n_nrn):
            n_spikes = trains[n].shape[0]
            new_rates[n] = int(round( n_spikes*1000.0/simtime ))
            print n,":",n_spikes, new_rates[n]
#         if(nseg==0):
#             save_train = pop_ex.get_data('spikes').segments[nseg].spiketrains
#         print save_train
        print nseg, dr_r
#         for i in range(nseg+1):
#             print i, pop_ex.get_data('spikes').segments[i].spiketrains

#         for n in range(n_nrn):
#             n_spikes2 = pop_src2.get_data('spikes').segments[nseg].spiketrains[n].shape[0]
#             print "drive spikes ",n, ":", n_spikes2
#         for n in range(n_nrn):
#             n_spikes0 = pop_src.get_data('spikes').segments[nseg].spiketrains[n].shape[0]
#             print "input spikes ",n, ":", n_spikes0
        nseg = nseg+1
        new_w = proj.get('weight', format='list', with_address=False)

        print "new w", new_w
        for n in range(n_nrn):
            if new_rates[n]>max_out_rate:
                continue
            if((w0*w_mult-th_w*w_mult)*(new_w[n] - th_w*w_mult)<0):
                n_trans[new_rates[n]] = n_trans[new_rates[n]] + 1
            n_tot[new_rates[n]] = n_tot[new_rates[n]] + 1

        p.reset()
    probs = n_trans / n_tot
    probs.tofile(output_file+"_"+str(r)+output_ext, sep='\t', format='%10.5f')




#p.run(50)
probs = n_trans / n_tot

print probs

probs.tofile(output_file+"_full"+output_ext, sep='\t', format='%10.5f')

xs = np.arange(max_out_rate+1)
series1 = np.array(probs).astype(np.double)
s1mask = np.isfinite(series1)

plt.plot(xs[s1mask], series1[s1mask], linestyle='-', marker='o')

plt.show()



p.end()
print "\n job done"