import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from matplotlib.pyplot import legend
from idna.core import _alabel_prefix

import matplotlib.pyplot as plt
import sys

from neo.io import PyNNNumpyIO
from neo.io import AsciiSpikeTrainIO
from neo.io import PyNNTextIO
from example_graph_params import *
import time

def gen_poisson_spikes(rate, simtime):
    spiketimes = []
    prob = 0.001*rate
    for i in xrange(simtime):
        if random.random() < prob:
            spiketimes.append(i)
    return spiketimes

timestr = time.strftime("%Y%m%d-%H%M%S")

to_plot_wgts = False

p.setup(1)

simtime = 300
n_runs = 1
w0 = 0.0
pre_rate = 50
drive_rates = np.arange(100, 180, 20) # driving source rates
n_rates = drive_rates.size
max_out_rate = 200
output_file = "data/dr2out_"+timestr
output_ext = ".txt"

avg_out_rate = np.zeros(n_rates) # number of weight transitions for each spiking rate of the output neuron for 0 to 200

n_nrn = 1  # total number of neurons in each run

pop_src = p.Population(n_nrn, p.SpikeSourcePoisson(rate=pre_rate), label="src")
pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=100), label="drive")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}
pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")
#pop_ex = p.Population(n_nrn, p.IF_curr_exp(), label="test")


syn_plas = p.STDPMechanism(
     timing_dependence = p.PreOnly(A_plus = 0.15*w_max*w_mult, A_minus = 0.15*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
        weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=w0*w_mult, delay=1.0)


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

pop_src.record('spikes')
pop_src2.record(['spikes'])
pop_ex.record('spikes')
nseg = 0
save_train = []


for ri in range(n_rates):
    dr_r = drive_rates[ri]
    pop_src2.set(rate=dr_r)
    for r in range(n_runs):
        p.run(simtime)
        new_rates = np.zeros(n_nrn, dtype=int)


#        trains = pop_ex.get_data('spikes').segments[nseg].spiketrains
        trains = pop_ex.get_data('spikes').segments[nseg].spiketrains
#         trains2 = pop_src2.get_data('spikes')
#         trains2 = trains2.segments[nseg].spiketrains

        for n in range(n_nrn):
            n_spikes = trains[n].shape[0]
            print dr_r, n,":", trains[n]
            print n_spikes
            #n_spikes2 = trains2[n].shape[0]
            #print n_spikes2
            avg_out_rate[ri] = avg_out_rate[ri] + n_spikes



        print nseg, dr_r
        nseg = nseg+1
        #new_w = proj.get('weight', format='list', with_address=False)


        p.reset()
#    probs.tofile(output_file+"_"+str(r)+output_ext, sep='\t', format='%10.5f')



#p.run(50)
avg_out_rate = avg_out_rate/n_nrn/n_runs*1000.0/simtime

print avg_out_rate
avg_out_rate.tofile(output_file+"_full"+output_ext, sep='\t', format='%10.5f')

xs = drive_rates
series1 = np.array(avg_out_rate).astype(np.double)
s1mask = np.isfinite(series1)

plt.plot(xs[s1mask], series1[s1mask], linestyle='-', marker='o')

plt.show()



p.end()
print "\n job done"