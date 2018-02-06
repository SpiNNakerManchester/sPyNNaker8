# Figure 2 with output frequency calculated as expected value of drive and input frequency
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from scipy.interpolate import interp1d
from matplotlib.pyplot import legend
from idna.core import _alabel_prefix

import matplotlib.pyplot as plt

from neo.io import PyNNNumpyIO
from neo.io import AsciiSpikeTrainIO
from neo.io import PyNNTextIO
from example_graph_params import *
import time

timestr = time.strftime("%Y%m%d-%H%M%S")


p.setup(1)

simtime = 300
n_runs = 30
w0 = 0.0 #initial weight for LTP
#w0 = 1.0 #initial weight for LTD
pre_rates = np.arange(40, 55, 10) # pre-synaptic neuron rates
n_pre_rates = pre_rates.shape[0]
drive_rates = np.arange(0, 400, 40) # driving source rates for LTPS
#drive_rates = np.arange(0, 300, 30) # driving source rates for LTDS
n_drive_rates = drive_rates.shape[0]
n_rates = drive_rates.size
max_out_rate = 200
output_file = "data2/fig2_"+timestr
output_ext = ".txt"

n_trans = np.zeros((n_pre_rates, n_drive_rates)) # number of weight transitions for each spiking rate of the output neuron for 0 to 200
n_tot = np.zeros((n_pre_rates, n_drive_rates)) # number of sims ran for each spiking rate of the output neuron (needed to calculate transition probability)

drx = np.arange(0, 400, 10)
dr2outfr = [   0, 0.16648148,    1.1612963,     3.11944444,    6.05296296,    9.62148148,
   13.60481481,   18.06703704,   22.73611111,   27.66277778,   32.37333333,
   37.15925926,   42.28777778,   47.39092593,   52.21037037,   57.26425926,
   61.97962963,   66.96407407,   71.48166667,   76.44574074,   81.01722222,
   85.62555556,   90.29092593,   94.64685185,   99.34407407,  103.56796296,
  107.85648148,  112.16888889,  116.34796296,  120.6287037,   124.61203704,
  128.63907407,  132.65185185,  136.53388889,  140.15388889,  143.59981481,
  146.63222222,  149.14685185,  151.49296296,  153.66962963]

f_dr2out = interp1d(drx, dr2outfr)


n_nrn = 200 # total number of neurons in each population

cell_params = {"i_offset":0.0,  "tau_ca2":175, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}

pops = []
pops_src = []
pops_src2 = []
projections = []

for pre_r in pre_rates:
    for dr_r in drive_rates:
        pop_src = p.Population(n_nrn, p.SpikeSourcePoisson(rate=pre_r), label="src")
        pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=dr_r), label="drive")
        pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")

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


        pop_ex.record(['spikes'])
        pops.append(pop_ex)
        pops_src.append(pop_src)
        pops_src2.append(pop_src2)
        projections.append(proj)
#         pop_src.record('spikes')
#         pop_src2.record('spikes')
nseg = 0
save_train = []
npops = len(pops)

for r in range(n_runs):
    p.run(simtime)
    new_rates = np.zeros(n_nrn, dtype=int)
    for i in range(npops):
        proj = projections[i]

        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates

        new_w = proj.get('weight', format='list', with_address=False)

        for n in range(n_nrn):

            if((w0*w_mult-th_w*w_mult)*(new_w[n] - th_w*w_mult)<0):
                n_trans[pre_rate_ind][dr_rate_ind] = n_trans[pre_rate_ind][dr_rate_ind] + 1
            n_tot[pre_rate_ind][dr_rate_ind] = n_tot[pre_rate_ind][dr_rate_ind] + 1


    nseg = nseg+1

    p.reset()
    probs = n_trans / n_tot
    probs.tofile(output_file+"_"+str(r)+output_ext, sep='\t', format='%10.5f')

    # need to reset the poisson sources, otherwise spike trains repeat too often
    for i in range(npops):
        pop_src = pops_src[i]
        pop_src2 = pops_src2[i]
        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates
        pop_src.set(rate=pre_rates[pre_rate_ind])
        pop_src2.set(rate=drive_rates[dr_rate_ind])





#p.run(50)
probs = n_trans / n_tot

print probs

probs.tofile(output_file+"_full"+output_ext, sep='\t', format='%10.5f')

xs = f_dr2out(drive_rates)

for i in range(n_pre_rates):
    if(w0!=0):
        xs = f_dr2out(drive_rates+pre_rates[i]) # add input neuron rates to drive rates, to get the expected output rate from all input spikes

    plt.plot(np.append([0], xs), np.append([0], probs[i, :]), linestyle='-', marker='o')

plt.show()



p.end()
print "\n job done"