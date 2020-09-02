from __future__ import print_function
import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


p.setup(1) # simulation timestep (ms)
runtime = 1000

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0 # DC input
                 }

# Learning parameters
min_weight = 0
max_weight = 0.1
pot_alpha = 0.01 # this is alpha in the paper

beta = 11
sigma = 201
initial_weight = 0.005

plastic_delay = 4

vestibular_neuclei = p.Population(1, # number of neurons
                       p.extra_models.IFCondExpCerebellum(**neuron_params),  # Neuron model
                       label="Vestibular Nuclei" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [1, 101, 201, 301, 401, 501, 601, 701, 801, 901]

mossy_fibre_src = p.Population(1, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )


# Create projection from MF to VN
mfvn_plas = p.STDPMechanism(
    timing_dependence=p.extra_models.TimingDependenceMFVN(beta=beta,
                                                          sigma=sigma),
    weight_dependence=p.extra_models.WeightDependenceMFVN(w_min=min_weight,
                                                          w_max=max_weight,
                                                          pot_alpha=pot_alpha),
    weight=initial_weight, delay=plastic_delay)

synapse_mfvn = p.Projection(
    mossy_fibre_src, vestibular_neuclei, p.AllToAllConnector(),
    synapse_type=mfvn_plas, receptor_type="excitatory")


mossy_fibre_src.record('spikes')
vestibular_neuclei.record("all")


mf_weights = []
for i in range(len(spike_times)):
    p.run(100)
    mf_weights.append(synapse_mfvn.get('weight', 'list', with_address=False))

mossy_fibre_src_spikes = mossy_fibre_src.get_data('spikes')
vestibular_neuclei_data = vestibular_neuclei.get_data()

# print weight history
for i in mf_weights:
    print(i)

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(mossy_fibre_src_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(vestibular_neuclei_data.segments[0].filter(name='v')[0],
          ylabel="VN membrane potential (mV)",
          data_labels=[vestibular_neuclei.label], yticks=True, xlim=(0, runtime)),
    Panel(vestibular_neuclei_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="VN excitatory current (mV)",
          data_labels=[vestibular_neuclei.label], yticks=True, xlim=(0, runtime)),
    Panel(vestibular_neuclei_data.segments[0].spiketrains,
          xlabel="Time (ms)",
          yticks=True, markersize=2, xlim=(0, runtime)),
    )


plt.savefig("single_vn_test.png", dpi=600)
plt.show()
p.end()

print("Job Complete")
