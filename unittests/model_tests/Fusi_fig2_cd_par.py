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
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
figname = "w18"

do_LTP = True # true for LTPs, false for LTDs
#do_LTP = False # true for LTPs, false for LTDs
do_save=False # save the data or not

p.setup(1)
p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpCa2Concentration, 200)

simtime = 300
n_runs = 20

w0 = 0.0
w_mult=2.0/16
a_plus = 0.15
a_minus = 0.15
w_min = 0.0
w_max = 1.0
w_drift = .0035
th_w = 0.50
V_th = -54.0
Ca_th_l = 3.0
Ca_th_h1 = 4.0
Ca_th_h2 = 13.0

scale_sys = 1.0

V_th = V_th * scale_sys


if do_LTP:
    w0 = 0.0 #initial weight for LTP
    drive_rates = np.arange(0, 400, 10) # driving source rates for LTPS
    drive_rates = np.arange(0, 300, 30) # driving source rates for LTPS
else:
    w0 = 1.0 #initial weight for LTD
    drive_rates = np.arange(0, 200, 5) # driving source rates for LTDS
    #drive_rates = np.arange(0, 200, 10) # driving source rates for LTDS


pre_rates = np.arange(5, 55, 5) # pre-synaptic neuron rates
pre_rates = np.arange(40, 55, 10) # pre-synaptic neuron rates
n_pre_rates = pre_rates.shape[0]

#drive_rates = np.arange(0, 150, 15) # driving source rates
n_drive_rates = drive_rates.shape[0]
n_rates = drive_rates.size
max_out_rate = 200
output_file = "data2/fig2_"+timestr
output_ext = ".txt"

n_trans = np.zeros((n_pre_rates, max_out_rate+1)) # number of weight transitions for each spiking rate of the output neuron for 0 to 200
n_tot = np.zeros((n_pre_rates, max_out_rate+1)) # number of sims ran for each spiking rate of the output neuron (needed to calculate transition probability)


n_nrn = 200 # total number of neurons in each population

cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65*scale_sys, 'v_rest':-65*scale_sys, 'v_thresh': -50*scale_sys}

pops = []
pops_src = []
pops_src2 = []
projections = []

for pre_r in pre_rates:
    for dr_r in drive_rates:
        pop_src = p.Population(n_nrn, p.SpikeSourcePoisson(rate=pre_r), label="src")
        pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=dr_r), label="drive")
        pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params,  label="test")
        pop_ex.initialize(v=-65*scale_sys)

        syn_plas = p.STDPMechanism(
            timing_dependence = p.PreOnly(A_plus = a_plus*w_max*w_mult, A_minus = a_minus*w_max*w_mult, th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2, th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
            weight_dependence = p.WeightDependenceFusi(w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult, th_w=th_w * w_mult), weight=w0*w_mult, delay=1.0)

        proj = p.Projection(
            pop_src,
            pop_ex,
            p.OneToOneConnector(),
            synapse_type=syn_plas, receptor_type='excitatory'
            )

        proj2 = p.Projection(pop_src2,  pop_ex,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=2.0*scale_sys),  receptor_type='excitatory')


        pop_ex.record(['spikes'])
        pops.append(pop_ex)
        pops_src.append(pop_src)
        pops_src2.append(pop_src2)
        projections.append(proj)
#         pop_src.record('spikes')
#         pop_src2.record('spikes')
nseg = 0
weights = []
npops = len(pops)

for r in range(n_runs):
    if r>0:
        p.reset()
    # need to reset the poisson sources, otherwise spike trains repeat too often
    for i in range(npops):
        pop_src = pops_src[i]
        pop_src2 = pops_src2[i]
        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates
        pop_src.set(rate=pre_rates[pre_rate_ind])
        pop_src2.set(rate=drive_rates[dr_rate_ind])
        pop_ex = pops[i]
        pop_ex.initialize(v=-65*scale_sys)

    p.run(simtime)
    new_rates = np.zeros(n_nrn, dtype=int)
    for i in range(npops):
        pop_ex = pops[i]
        proj = projections[i]

        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates

        #trains = pop_ex.get_data('spikes').segments[nseg].spiketrains
        new_w = proj.get('weight', format='list', with_address=False)
        weights.append(new_w)



    nseg = nseg+1





for i in range(npops):
    pop_ex = pops[i]
    alltrains = pop_ex.get_data('spikes').segments
    for nseg in range(n_runs):
        trains = alltrains[nseg].spiketrains
        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates
        new_w = weights[nseg*npops+i]
        #print new_w, "xxx"
        #print "pre",pre_rates[pre_rate_ind]
        #print "dr", drive_rates[dr_rate_ind]
        for n in range(n_nrn):
            n_spikes = trains[n].shape[0]
            new_rate = int(round( n_spikes*1000.0/simtime ))
            #print n,":",n_spikes, new_rate

            if new_rate>max_out_rate:
                continue
            if((w0*w_mult-th_w*w_mult)*(new_w[n] - th_w*w_mult)<0):
                n_trans[pre_rate_ind][new_rate] = n_trans[pre_rate_ind][new_rate] + 1
            n_tot[pre_rate_ind][new_rate] = n_tot[pre_rate_ind][new_rate] + 1




#p.run(50)

p.end()

probs = n_trans / n_tot

print probs

if do_save:
    probs.tofile(output_file+"_full"+output_ext, sep='\t', format='%10.5f')

xs = np.arange(max_out_rate+1)
series1 = np.array(probs).astype(np.double)
s1mask = np.isfinite(series1)
print s1mask
#xs = np.tile(xs, (n_pre_rates,1))
print xs[s1mask[0,:]]

for i in range(n_pre_rates):
    plt.plot(xs[s1mask[i,:]], series1[i,:][s1mask[i,:]], linestyle='-', marker='o')

plt.savefig('./figs/' + "figure_2_"+figname+"_"+timestr+'.png', format="png")
plt.show()
plt.close()



print "\n job done"