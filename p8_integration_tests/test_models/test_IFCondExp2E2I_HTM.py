import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
from signal_prep import *
p.setup(1.)
runtime = 1000
num_repeats = 1.
column_size = 16

active_spikes = [i for i in range(10,runtime,100)]
prediction_spikes = [i-10. for i in active_spikes if i > 300.]

# Spike source to send spike via plastic synapse
exc_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': prediction_spikes}, label="src1")
exc2_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': active_spikes}, label="src2")
# inh_src = p.Population(1, p.SpikeSourceArray,
#                           {'spike_times': [30]}, label="src3")
# inh2_src = p.Population(1, p.SpikeSourceArray,
#                           {'spike_times': [160]}, label="src4")

# Post-synapse population
# pop_exc = p.Population(column_size, p.extra_models.IFCondExp2E2I(),  label="test")
# pop_exc = p.Population(column_size, p.IF_cond_exp,  label="test")
pop_exc = p.Population(column_size, p.IF_curr_exp,  label="test")

# pop_exc.set(e_rev_E=-55)
# pop_exc.set(tau_syn_E=50)
# pop_exc.set(tau_syn_E2=5)

# pop_exc.set(e_rev_E2=-10)
# pop_exc.set(e_rev_E2=-80)
# pop_exc.set(e_rev_E2=-50)

stdp_model = p.STDPMechanism(
        timing_dependence=p.SpikePairRule(
            tau_plus=16., tau_minus=30., A_plus=0.1, A_minus=0.1),
        weight_dependence=p.AdditiveWeightDependence(
            # w_min=0., w_max=0.2), weight=0.1,delay=1.)
            w_min=0., w_max=3.0), weight=2.,delay=1.)

# synapse_exc = p.Projection(
#     exc_src, pop_exc, p.OneToOneConnector(),
#     p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")
#     # synapse_type=stdp_model, receptor_type="excitatory")


synapse_exc2 = p.Projection(
    exc2_src, pop_exc, p.AllToAllConnector(),
    # p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory2")
    synapse_type=stdp_model, receptor_type="excitatory")

inh_connection_list = []
winh = 0.2
for post in range(column_size):
    for pre in range(column_size):
        if pre!=post:
            inh_connection_list.append((pre,post))
# active_inh_active_projection = p.Projection(pop_exc,pop_exc,p.FromListConnector(inh_connection_list),
#                                               synapse_type=p.StaticSynapse(weight=winh),receptor_type='inhibitory')

# synapse_inh = p.Projection(
#     inh_src, pop_exc, p.OneToOneConnector(),
#     p.StaticSynapse(weight=0.33, delay=1), receptor_type="inhibitory")
# synapse_inh2 = p.Projection(
#     inh2_src, pop_exc, p.AllToAllConnector(),
#     p.StaticSynapse(weight=1.32, delay=1), receptor_type="inhibitory2")

pop_exc.record("all")
weights = []
for _ in range(int(num_repeats)):
    p.run(runtime/num_repeats)
    # runtime = runtime/0.1 # temporary scaling to account for new recording
    weights.append(synapse_exc2.get('weight', 'list',
                                       with_address=False)[0])

exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

print "weights",weights
p.end()
# Plot
Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",legend=False,
          yticks=True,xticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",legend=False,
           yticks=True,xticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",legend=False,
           yticks=True,xticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,marker='.',
          yticks=True,markersize=3,
                 markerfacecolor='black', markeredgecolor='none',
                 markeredgewidth=0,xticks=True, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
        len(exc_data.segments[0].spiketrains[0]))
)

recorded_active_spikes = [spike_time.item() for spike_time in exc_data.segments[0].spiketrains[0]]

# spike_raster_plot_8([recorded_active_spikes,prediction_spikes],plt,runtime/1000.,ylim=3.)
plt.figure()
plt.subplot(2,1,1)
plt.eventplot([recorded_active_spikes,active_spikes],colors=['b','r'])

plt.subplot(2,1,2)
x = np.linspace(0,runtime,num_repeats)
plt.plot(x,weights)

plt.show()