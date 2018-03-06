import spynnaker8 as p
import matplotlib
matplotlib.use('Agg')
import numpy as np
from neo.core.spiketrain import SpikeTrain
from scipy.ndimage.measurements import label
from matplotlib.pyplot import legend
from pyNN.utility.plotting import Figure, Panel, DataTable
import matplotlib.pyplot as plt
from idna.core import _alabel_prefix

from neo.io import PyNNNumpyIO
from neo.io import AsciiSpikeTrainIO
from neo.io import PyNNTextIO
import time

#plt.ioff()  # turn on if running a long sim over ssh

timestr = time.strftime("%Y%m%d-%H%M%S")

figname0 =  "LTPtst"
figname = './figs/' + "figure_2_"+figname0+"_"+timestr+'.png'
figname2 = './figs/' + "figure_2_inset_"+figname0+"_"+timestr+'.png'

output_file = "data2/fig2_"+timestr
output_ext = ".txt"
output_file_name = output_file+"_full"+output_ext

do_LTP = True # true for LTPs, false for LTDs
#do_LTP = False # true for LTPs, false for LTDs
do_save = False # save the data or not
spinn3 = True  # True if using 4 node board (resources are limited)

p.setup(1)
p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpCa2Concentration, 200)

simtime = 300
n_runs = 2
if spinn3:
    n_nrn = 200 # total number of neurons in each population
else:
    n_nrn = 1000

w0 = 0.0
w_mult=2.0/4   # this parameters scales all weight variables, actual w_max = w_mult; should be 0.1-0.125 or smaller to avoid distortions in results
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

V_th = V_th


if do_LTP:
    w0 = 0.0 #initial weight for LTP
    if spinn3:
        drive_rates = np.arange(0, 300, 30) # driving source rates for LTPS
    else:
        drive_rates = np.arange(0, 400, 10) # driving source rates for LTPS
else:
    w0 = 1.0 #initial weight for LTD
    if spinn3:
        drive_rates = np.arange(0, 200, 20) # driving source rates for LTDS
    else:
        drive_rates = np.arange(0, 200, 5) # driving source rates for LTDS

n_drive_rates = drive_rates.shape[0]


if spinn3:
    pre_rates = np.arange(40, 55, 10) # pre-synaptic neuron rates
else:
    pre_rates = np.arange(10, 55, 10) # pre-synaptic neuron rates

n_pre_rates = pre_rates.shape[0]



max_out_rate = 200 # ignore output rates above 200

n_trans = np.zeros((n_pre_rates, max_out_rate+1)) # number of weight transitions for each spiking rate of the output neuron for 0 to 200
n_tot = np.zeros((n_pre_rates, max_out_rate+1)) # number of sims ran for each spiking rate of the output neuron (needed to calculate transition probability)



cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65 , 'v_rest':-65 , 'v_thresh': -50 }

pops = []
pops_src = []
pops_src2 = []
projections = []

# set up populations for all combinations of sriving and input rates
for pre_r in pre_rates:
    for dr_r in drive_rates:
        pop_src = p.Population(n_nrn, p.SpikeSourcePoisson(rate=pre_r), label="src")
        pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=dr_r), label="drive")
        pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params,  label="test")
        pop_ex.initialize(v=-65 )

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
               synapse_type=p.StaticSynapse(weight=2.0 ),  receptor_type='excitatory')


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

# make n_runs runs, collect weights after each run
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
        pop_ex.initialize(v=-65)

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




# extract output spikes and calculate synaptic transition data
for i in range(npops):
    pop_ex = pops[i]
    alltrains = pop_ex.get_data('spikes').segments
    for nseg in range(n_runs):
        trains = alltrains[nseg].spiketrains
        pre_rate_ind = i / n_drive_rates
        dr_rate_ind = i - pre_rate_ind * n_drive_rates
        new_w = weights[nseg*npops+i]
        for n in range(n_nrn):
            n_spikes = trains[n].shape[0]   # count spikes for neuron n in run nseg
            new_rate = int(round( n_spikes*1000.0/simtime ))  # output rate per second for this neuron & run
            #print n,":",n_spikes, new_rate

            if new_rate>max_out_rate:
                continue
            if((w0*w_mult-th_w*w_mult)*(new_w[n] - th_w*w_mult)<0):   # if weight crossed the threshold, update transition data
                n_trans[pre_rate_ind][new_rate] = n_trans[pre_rate_ind][new_rate] + 1
            n_tot[pre_rate_ind][new_rate] = n_tot[pre_rate_ind][new_rate] + 1





p.end()

# transition probabilities are equal to number of transitions / number of runs for each presynaptic rate and output rate pair
probs = n_trans / n_tot


if do_save:
    probs.tofile(output_file_name, sep='\t', format='%10.5f')

xs = np.arange(max_out_rate+1)
series1 = np.array(probs).astype(np.double)
s1mask = np.isfinite(series1)  # mask infinite values

fig_settings = {
    'lines.linewidth': 1,
    'axes.linewidth': 1,
    'axes.labelsize': 16,
    'legend.fontsize': 'small',
    'font.size': 12
}
plt.rcParams.update(fig_settings)


if do_LTP:
    plt.ylabel(r'${\mathrm{P_{LTP}}}$')
else:
    plt.ylabel(r'${\mathrm{P_{LTD}}}$')
plt.xlabel(r'${\mathrm{\nu_{post}}}$')

# make plot of P_LT(P/D) against output firing rate
max_probs = np.zeros((n_pre_rates,1))
for i in range(n_pre_rates):
    plt.plot(xs[s1mask[i,:]], series1[i,:][s1mask[i,:]], linestyle='-', marker='o')
    max_probs[i] = np.amax(series1[i,:][s1mask[i,:]])

plt.savefig(figname, format="png")
plt.tight_layout()
plt.clf()

# make plot of max P_LT(P/D) against input firing rate
if do_LTP:
    plt.ylabel(r'${\mathrm{max(P_{LTP})}}$')
else:
    plt.ylabel(r'${\mathrm{max(P_{LTD})}}$')
plt.xlabel(r'${\mathrm{\nu_{pre}}}$')
plt.plot(pre_rates, max_probs, linestyle='-', marker='o')
plt.savefig(figname2, format="png")


#plt.show()
plt.close()



print "\n job done"
