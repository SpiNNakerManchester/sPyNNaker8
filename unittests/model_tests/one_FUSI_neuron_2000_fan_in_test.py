import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(0.1)
runtime = 1000
initial_run = 15  # to negate any initial conditions

# STDP parameters
a_plus = 0.01
a_minus = 0.01
tau_plus = 20
tau_minus = 20
plastic_delay = 3
initial_weight = 2.5
max_weight = 5
min_weight = 0

# spike_times = [1]
# # Spike source to send spike via plastic synapse
# pop_src1 = p.Population(1, p.SpikeSourceArray,
#                         {'spike_times': spike_times}, label="src1")

pop_src1 = p.Population(1600, p.SpikeSourcePoisson(rate=2, duration=runtime))
pop_src2 = p.Population(400, p.SpikeSourcePoisson(rate=50, duration=runtime))

# Post-synapse population
# pop_exc = p.Population(1, p.IF_curr_exp(),  label="test")
cell_params = {"i_offset":0.0,  "tau_ca2":150, "i_alpha":1., "i_ca2":3.,  'v_reset':-65}
pop_exc= p.Population(1, p.extra_models.IFCurrExpCa2Concentration,cell_params, label="Fusi Neuron")

# # Create Static Projections
# s_proj = p.Projection(
#     pop_src1, pop_exc, p.AllToAllConnector(),
#     p.StaticSynapse(weight=0.01, delay=1), receptor_type="excitatory")
# s_proj2 = p.Projection(
#     pop_src2, pop_exc, p.AllToAllConnector(),
#     p.StaticSynapse(weight=0.01, delay=1), receptor_type="excitatory")

# Create Plastic Projections
w_min = 0.0
w_max = 0.01
w0 = 0.01
w_drift = .000035
th_w = 0.0050
w_mult = 1.0
V_th = -54.0
Ca_th_l = 3.0
Ca_th_h1 = 4.0
Ca_th_h2 = 13.

syn_plas = p.STDPMechanism(
    timing_dependence = p.PreOnly(
        A_plus = 0.15*w_max*w_mult, A_minus = 0.15*w_max*w_mult,
        th_v_mem=V_th, th_ca_up_l = Ca_th_l, th_ca_up_h = Ca_th_h2,
        th_ca_dn_l = Ca_th_l, th_ca_dn_h = Ca_th_h1),
    weight_dependence = p.WeightDependenceFusi(
        w_min=w_min*w_mult, w_max=w_max*w_mult, w_drift=w_drift*w_mult,
        th_w=th_w * w_mult),
    weight=w0*w_mult, delay=1.0)

proj = p.Projection(
    pop_src1,
    pop_exc,
    p.AllToAllConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

proj2 = p.Projection(
    pop_src2,
    pop_exc,
    p.AllToAllConnector(),
    synapse_type=syn_plas, receptor_type='excitatory'
    )

pop_src1.record('all')
pop_src2.record('all')
pop_exc.record("all")
p.run(initial_run + runtime)
weights = []

# weights.append(proj.get('weight', 'list',
#                                    with_address=False)[0])

pre_spikes_slow = pop_src1.get_data('spikes')
pre_spikes_fast = pop_src2.get_data('spikes')
exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(pre_spikes_slow.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    Panel(pre_spikes_fast.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (nA)",
          data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
#           ylabel="gsyn inhibitory (mV)",
#           data_labels=[pop_src1.label], yticks=True, xlim=(0, runtime)),
#     Panel(exc_data.segments[0].spiketrains,
#           yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
p.end()


