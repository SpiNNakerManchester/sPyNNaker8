# Calculate average output rate for a range of drive rates
# the network consists of one Fusi neuron, and one driving Poisson source, connected with a static connection, repeated 6000 times
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

def print_spikes(trains):
    nseg = len(trains.segments)
    for i in range(nseg):
        trains1 = trains.segments[i].spiketrains
        print "segment ", i,
        for j in range(len(trains1)):
            print "nrn ", j, " ", trains1[j]


timestr = time.strftime("%Y%m%d-%H%M%S")

to_plot_wgts = False

p.setup(1)

simtime = 300
n_runs = 3
drive_rates = np.arange(10, 400, 10) # driving source rates
n_rates = drive_rates.size
output_file = "data/dr2out_"+timestr
output_ext = ".txt"

avg_out_rate = np.zeros(n_rates) # calculated average output rate for each drive rate

n_nrn = 6000  # total number of neurons in each run

p.set_number_of_neurons_per_core(p.extra_models.IFCurrExpCa2Concentration, 200)


pop_src2 = p.Population(n_nrn, p.SpikeSourcePoisson(rate=100), label="drive")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}
pop_ex = p.Population(n_nrn, p.extra_models.IFCurrExpCa2Concentration, cell_params, label="test")

proj2 = p.Projection(pop_src2,  pop_ex,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=3.0),  receptor_type='excitatory')

pop_src2.record(['spikes'])
pop_ex.record('spikes')
nseg = 0
save_train = []


for ri in range(n_rates):
    dr_r = drive_rates[ri]
    for r in range(n_runs):
        pop_src2.set(rate=dr_r)
        p.run(simtime)
        new_rates = np.zeros(n_nrn, dtype=int)

        trains2 = pop_src2.get_data('spikes')
        trains2 = trains2.segments[nseg].spiketrains


        trains = pop_ex.get_data('spikes').segments[nseg].spiketrains

        for n in range(n_nrn):
            n_spikes = trains[n].shape[0]
            #print dr_r, n,":", trains[n]
            print n_spikes
            n_spikes2 = trains2[n].shape[0]
            print n_spikes2
            avg_out_rate[ri] = avg_out_rate[ri] + n_spikes



        print nseg, dr_r
        nseg = nseg+1


        p.reset()


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