import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(0.1)
runtime = 1000

# Spike source to send spike via plastic synapse
exc_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [10]}, label="src1")
exc2_src = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [60]}, label="src2")
inh_src = p.Population(1, p.SpikeSourceArray,
                          {'spike_times': [30]}, label="src3")
inh2_src = p.Population(1, p.SpikeSourceArray,
                          {'spike_times': [160]}, label="src4")

# Post-synapse population
pop_exc = p.Population(1, p.extra_models.IFCondExp2E2I(),  label="test")

pop_exc.set(e_rev_E=-5)
pop_exc.set(e_rev_E2=-10)
pop_exc.set(e_rev_E2=-80)
pop_exc.set(e_rev_E2=-50)



synapse_exc = p.Projection(
    exc_src, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory2")
synapse_exc2 = p.Projection(
    exc2_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=.1, delay=1), receptor_type="excitatory")
synapse_inh = p.Projection(
    inh_src, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=0.33, delay=1), receptor_type="inhibitory2")
synapse_inh2 = p.Projection(
    inh2_src, pop_exc, p.AllToAllConnector(),
    p.StaticSynapse(weight=1.32, delay=1), receptor_type="inhibitory")

pop_exc.record("all")
p.run(runtime)
weights = []

# runtime = runtime/0.1 # temporary scaling to account for new recording
# weights.append(synapse_inh2.get('weight', 'list',
#                                    with_address=False)[0])

exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
        len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
# p.end()