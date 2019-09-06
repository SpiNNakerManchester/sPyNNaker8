from __future__ import print_function
import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 500

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0 # DC input
                 }

# Learning parameters
pot_alpha = 0.01
beta = 11
sigma = 201

pot_alpha = 0.01
min_weight = 0
max_weight = 0.1

initial_weight = 0.01
plastic_delay = 4

vestibular_nuclei = p.Population(1, # number of neurons
                       p.extra_models.IFCondExpCerebellum(**neuron_params),  # Neuron model
                       label="Vestibular Nuclei" # identifier
                       )


# Spike source to send spike via synapse
mf_spike_times = [50, 60, 65]#, 150, 175, 180, 190, 240, 250, 255,
#                270, 300, 345, 350, 360, 370, 400, 422, 425, 427, 429]

mossy_fibre_src = p.Population(1, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': mf_spike_times}, # source spike times
                        label="src1" # identifier
                        )

# Spike source to send spike via synapse from climbing fibre
pc_spike_times = [60]#, 104, 107, 246]
purkinje_cell_src = p.Population(1, # number of sources
                        p.SpikeSourceArray, # source type
                        {'spike_times': pc_spike_times}, # source spike times
                        label="purkinje_cell_src" # identifier
                        )

# Create projection from GC to PC
mfvn_plas = p.STDPMechanism(
    timing_dependence=p.extra_models.TimingDependenceMFVN(beta=beta,
                                                          sigma=sigma),
    weight_dependence=p.extra_models.WeightDependenceMFVN(w_min=min_weight,
                                                          w_max=max_weight,
                                                          pot_alpha=pot_alpha),
    weight=initial_weight, delay=plastic_delay)

synapse_mfvn = p.Projection(
    mossy_fibre_src, vestibular_nuclei, p.AllToAllConnector(),
    synapse_type=mfvn_plas, receptor_type="excitatory")


# Create projection from PC to VN
synapse = p.Projection(
    purkinje_cell_src, vestibular_nuclei, p.OneToOneConnector(),
    p.StaticSynapse(weight=0.0, delay=1), receptor_type="excitatory")


mossy_fibre_src.record('spikes')
purkinje_cell_src.record('spikes')
vestibular_nuclei.record("all")

p.run(runtime)

mossy_fibre_src_spikes = mossy_fibre_src.get_data('spikes')
purkinje_cell_src_spikes = purkinje_cell_src.get_data('spikes')
vestibular_nuclei_data = vestibular_nuclei.get_data()

mf_weights = synapse_mfvn.get('weight', 'list', with_address=False)
print("\n {}".format(mf_weights))

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(mossy_fibre_src_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(purkinje_cell_src_spikes.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(vestibular_nuclei_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[vestibular_nuclei.label], yticks=True, xlim=(0, runtime)),
    Panel(vestibular_nuclei_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[vestibular_nuclei.label], yticks=True, xlim=(0, runtime)),
    Panel(vestibular_nuclei_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    )


plt.show()
p.end()
print("Job Complete")


