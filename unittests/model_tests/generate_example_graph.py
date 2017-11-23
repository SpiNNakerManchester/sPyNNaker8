import matplotlib.pyplot as plt
import numpy as np
from neo import io

from example_graph_params import *

########################################
# data comes from the 'data' folder
# ca.txt contains ca concentrations
# wgt.txt contains time-unscaled weight pairs
# data.txt is V
# post_spikes.txt is output spikes
# pre_spikes.txt is input spikes
#######################################

r_pre = io.AsciiSpikeTrainIO(filename='data/pre_spikes.txt')
r_post = io.PyNNTextIO(filename='data/data.txt')
r_post_spikes = io.AsciiSpikeTrainIO(filename='data/post_spikes.txt')


pre_spikes = r_pre.read_segment()
post_spikes = r_post_spikes.read_segment()
V_data = r_post.read_segment() #.analogsignals[0]

csv = np.genfromtxt ('data/ca.txt')
Ca = csv[:]
print Ca
csv = np.genfromtxt ('data/wgt.txt')
w_time = csv[:,0]
wgts = csv[:,1]
print w_time, wgts

print post_spikes.spiketrains[0].shape

#import sys
#sys.exit(1)


fig_settings = {
    'lines.linewidth': 0.5,
    'axes.linewidth': 0.5,
    'axes.labelsize': 'small',
    'legend.fontsize': 'small',
    'font.size': 8
}
plt.rcParams.update(fig_settings)
plt.figure(1, figsize=(6, 8))
plt.suptitle("Synaptic transitions")


def plot_spiketrains(segment, label):
    for spiketrain in segment.spiketrains:
        y = np.ones_like(spiketrain) #* spiketrain.annotations['source_id']
        plt.plot(spiketrain, y, '|')
        plt.ylabel(label)
        plt.setp(plt.gca().get_xticklabels(), visible=False)


def plot_signal(signal, index, colour='b'):
    label = "Neuron " # % signal.annotations['source_ids'][index]
    plt.plot(signal.times, signal[:, index], colour, label=label)
    plt.ylabel("%s (%s)" % (signal.name, signal.units._dimensionality.string))
    plt.setp(plt.gca().get_xticklabels(), visible=False)
    plt.legend()

n_panels = 5
plt.subplot(n_panels, 1, 1)
plot_spiketrains(pre_spikes, "pre-spikes")
plt.subplot(n_panels, 1, 5)
plot_spiketrains(post_spikes, "post-spikes")
plt.subplot(n_panels, 1, 2)
plt.plot(range(simtime), V_data.analogsignals[0], 'b', label='V')
plt.plot((0, simtime), (V_th, V_th), 'r--')
plt.ylabel("V")

plt.subplot(n_panels, 1, 3)
plt.plot(w_time, wgts/weight_scale, 'b')
plt.ylabel("weights")
plt.ylim([0,1.000])
plt.xlim([0,1000])

plt.subplot(n_panels, 1, 4)
plt.plot(range(simtime), Ca, 'b')
plt.plot((0, simtime), (Ca_th_h2, Ca_th_h2), 'r--')
plt.plot((0, simtime), (Ca_th_h1, Ca_th_h1), 'g--')
plt.plot((0, simtime), (Ca_th_l, Ca_th_l), 'k--')
plt.ylabel("Ca")
#plot_signal(V_data, 0)
#plt.xlabel("time (%s)" % array.times.units._dimensionality.string)
#plt.setp(plt.gca().get_xticklabels(), visible=True)

plt.show()