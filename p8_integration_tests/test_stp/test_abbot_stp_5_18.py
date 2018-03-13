import spynnaker8 as p
import numpy as np
import scipy as sp
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks


# functions to compute the average release probability <P_rel>

def average_release_prob_facilitation(P_0, f, r, tau_P):

    return (P_0 + f*r*tau_P) / (1 + r*f*tau_P)


def average_release_prob_depression(P_0, f, r, tau_P):

    return P_0 / (1 + (1-f)*r*tau_P)



timestep = 1
p.setup(timestep)
# to scale runtime
rt_scaling = 10
initial_run = 100  # to negate any initial conditions

# STDP parameters
STP_type = 0 # 0 for depression; 1 for facilitation
f = 0.4
P_baseline = 1
tau_P = 500
baseline_weight = 1


poisson_input = False


spiking_frequencies = np.linspace(0, 100, 21)
runtime = len(spiking_frequencies)*200

timestamp = initial_run + 200*rt_scaling
if not poisson_input:
    spike_times = np.linspace(initial_run, timestamp, spiking_frequencies[0]*200*rt_scaling/1000.)
else:
    t = sp.arange(initial_run, timestamp)
    spike_times = t[np.random.rand(len(t)) < spiking_frequencies[0]/1000.]

for i in range(1, len(spiking_frequencies)):
    if not poisson_input:
        spike_times = np.concatenate((spike_times, np.linspace(timestamp,timestamp+200*rt_scaling,
                                                               spiking_frequencies[i]*200*rt_scaling/1000.)))
    else:
        t = sp.arange(timestamp, timestamp + 200*rt_scaling)
        spike_times = np.concatenate((spike_times, t[np.random.rand(len(t)) < spiking_frequencies[i]/1000.]))
    timestamp = timestamp + 200*rt_scaling


# Spike source to send spike via plastic synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")


# Post-synapse population
pop_exc = p.Population(1, p.IF_curr_exp(),  label="test")

# Create projections
# synapse = p.Projection(
#     pop_src1, pop_exc, p.AllToAllConnector(),
#     p.StaticSynapse(weight=0.01, delay=1), receptor_type="excitatory")

syn_plas = p.STDPMechanism(
        timing_dependence=p.AbbotSTP(STP_type, f, P_baseline, tau_P),
#       weight_dependence=p.MultiplicativeWeightDependence(),
        weight_dependence=p.STPOnlyWeightDependence(),
        weight=baseline_weight, delay=timestep)

synapse = p.Projection(pop_src1,
                        pop_exc,
                        p.OneToOneConnector(),
                        synapse_type=syn_plas)



pop_src1.record('all')
pop_exc.record("all")
p.run(initial_run + runtime*rt_scaling)
weights = []

weights.append(synapse.get('weight', 'list',
                                   with_address=False)[0])

pre_spikes_slow = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()

#print "Post-synaptic neuron firing frequency: {} Hz".format(
    #len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(pre_spikes_slow.segments[0].spiketrains,
          xlabel="Time (ms)", xticks=True,
          yticks=True, markersize=0.2, xlim=(0, runtime*rt_scaling)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          xlabel="Time (ms)", xticks=True,
          ylabel="Membrane potential (mV)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime*rt_scaling)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          xlabel="Time (ms)",xticks=True,
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime*rt_scaling)),
#     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
#           ylabel="gsyn inhibitory (mV)",
#           data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
#     annotations="Post-synaptic neuron firing frequency: {} Hz".format(
#     len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
#p.end()


