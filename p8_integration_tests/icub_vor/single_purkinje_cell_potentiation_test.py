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
pot_alpha = 0.002 # this is alpha in the paper

t_peak = 101 # ms

initial_weight = 0.05
plastic_delay = 4

purkinje_cell = p.Population(1, # number of neurons
                       p.extra_models.IFCondExpCerebellum(**neuron_params),  # Neuron model
                       label="Purkinje Cell" # identifier
                       )


# Spike source to send spike via synapse
spike_times = [101, 201, 301, 401, 501, 601, 701, 801, 901]

granular_cell = p.Population(1, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': spike_times}, # source spike times
                        label="src1" # identifier
                        )


# Create projection from GC to PC
pfpc_plas = p.STDPMechanism(
    timing_dependence=p.extra_models.TimingDependencePFPC(t_peak=t_peak),
    weight_dependence=p.extra_models.WeightDependencePFPC(w_min=min_weight,
                                                          w_max=max_weight,
                                                          pot_alpha=pot_alpha),
    weight=initial_weight, delay=plastic_delay)

synapse_pfpc = p.Projection(
    granular_cell, purkinje_cell, p.AllToAllConnector(),
    synapse_type=pfpc_plas, receptor_type="excitatory")




granular_cell.record('spikes')
purkinje_cell.record("all")


pf_weights = []
for i in range(len(spike_times)):
    p.run(100)
    pf_weights.append(synapse_pfpc.get('weight', 'list', with_address=False))

granluar_cell_spikes = granular_cell.get_data('spikes')
purkinje_data = purkinje_cell.get_data()

for i in pf_weights:
    print(i)
# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(granluar_cell_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(purkinje_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[purkinje_cell.label], yticks=True, xlim=(0, runtime)),
    Panel(purkinje_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[purkinje_cell.label], yticks=True, xlim=(0, runtime)),
    Panel(purkinje_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    )


plt.show()
p.end()

print("Job Complete")

