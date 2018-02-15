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
#from example_graph_params import *
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

do_LTP = True # true for LTPs, false for LTDs
#do_LTP = False # true for LTPs, false for LTDs
do_save=False # save the data or not

p.setup(1)
p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpCa2Concentration, 200)

w_min = 0.0
w_max = 1.0
w_drift = .0035
th_w = 0.50
w_mult = 2.0
V_th = -54.0
Ca_th_l = 3.0
Ca_th_h1 = 4.0
Ca_th_h2 = 13.0

simtime = 300
n_runs = 300
n_nrn = 200 # total number of neurons in each population

if do_LTP:
    w0 = 0.0 #initial weight for LTP
    drive_rates = np.arange(0, 400, 10) # driving source rates for LTPS
    #drive_rates = np.arange(100, 200, 20) # driving source rates for LTPS
else:
    w0 = 1.0 #initial weight for LTD
    drive_rates = np.arange(0, 200, 5) # driving source rates for LTDS
    #drive_rates = np.arange(0, 200, 10) # driving source rates for LTDS

w_mult  = 2.0
pre_rates = np.arange(5, 55, 5) # pre-synaptic neuron rates
#pre_rates = np.arange(30, 55, 10) # pre-synaptic neuron rates
n_pre_rates = pre_rates.shape[0]
n_drive_rates = drive_rates.shape[0]
n_rates = drive_rates.size
max_out_rate = 200
output_file = "data2/fig2_"+timestr
output_ext = ".txt"

n_trans = np.zeros((n_pre_rates, n_drive_rates)) # number of weight transitions for each spiking rate of the output neuron for 0 to 200
n_tot = np.zeros((n_pre_rates, n_drive_rates)) # number of sims ran for each spiking rate of the output neuron (needed to calculate transition probability)

drx = np.arange(0, 400, 10)
# output frequencies for driving frequencies from 0 to 400, with step 10 and no input
dr2outfr = [   0, 0.16648148,    1.1612963,     3.11944444,    6.05296296,    9.62148148,
   13.60481481,   18.06703704,   22.73611111,   27.66277778,   32.37333333,
   37.15925926,   42.28777778,   47.39092593,   52.21037037,   57.26425926,
   61.97962963,   66.96407407,   71.48166667,   76.44574074,   81.01722222,
   85.62555556,   90.29092593,   94.64685185,   99.34407407,  103.56796296,
  107.85648148,  112.16888889,  116.34796296,  120.6287037,   124.61203704,
  128.63907407,  132.65185185,  136.53388889,  140.15388889,  143.59981481,
  146.63222222,  149.14685185,  151.49296296,  153.66962963]

# for w=3.0
# dr2outfr = [0,    1.395,         4.96648148,    9.83666667,   15.55796296 ,  21.92481481,
#    28.54833333,   35.24277778,   42.14074074,   49.2487037,    56.06703704,
#    62.83759259,   69.6362963,    76.59666667,   82.91351852,   89.53481481,
#    95.93555556,  102.27685185,  108.46407407,  114.67666667,  120.56277778,
#   126.42537037,  132.31259259,  138.00407407,  143.53833333,  149.05981481,
#   154.3962963,   159.76666667,  164.79759259,  170.1087037,   174.76259259,
#   179.71462963,  184.59574074,  188.99555556,  193.78555556,  197.70277778,
#   201.16777778,  204.29333333,  206.75833333,  209.09314815]

f_dr2out = interp1d(drx, dr2outfr)



cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}

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
               synapse_type=p.StaticSynapse(weight=w_mult),  receptor_type='excitatory')


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
    if do_save:
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
if do_save:
    probs.tofile(output_file+"_full"+output_ext, sep='\t', format='%10.5f')

xs = f_dr2out(drive_rates)

for i in range(n_pre_rates):
    if(w0!=0):
        xs = f_dr2out(drive_rates+pre_rates[i]) # add input neuron rates to drive rates, to get the expected output rate from all input spikes

    plt.plot(np.append([0], xs), np.append([0], probs[i, :]), linestyle='-', marker='o')

# plt.show()

plt.plot(pre_rates, np.amax(probs, 1), linestyle='-', marker='o')
plt.savefig('./' + "figure_2"+'.png', format="png")
plt.close()
# plt.show()



p.end()
print "\n job done"