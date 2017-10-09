import spynnaker8 as p
import matplotlib.pyplot as plt
import pyNN.utility.plotting as plot

p.setup(0.1)
runtime = 50
populations = []
title = "PyNN0.8 alpha synapse testing"

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [[5, 10, 15, 20]]}, label="src1")

populations.append(p.Population(1, p.IF_curr_alpha, {}, label="test"))
populations[0].set(tau_syn_E=3)
populations[0].set(tau_syn_I=4)

# define the projections
exc_proj = p.Projection(pop_src1, populations[0],
                        p.OneToOneConnector(),
                        p.StaticSynapse(weight=1, delay=1),
                        receptor_type="excitatory")
inh_proj = p.Projection(pop_src1, populations[0],
                        p.OneToOneConnector(),
                        p.StaticSynapse(weight=1, delay=25),
                        receptor_type="inhibitory")

populations[0].record("all")
p.run(runtime)

v = populations[0].get_data("v")
gsyn_exc = populations[0].get_data("gsyn_exc")
gsyn_inh = populations[0].get_data("gsyn_inh")
spikes = populations[0].get_data("spikes")

plot.Figure(
    plot.Panel(v.segments[0].filter(name='v')[0],
               ylabel="Membrane potential (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    plot.Panel(gsyn_exc.segments[0].filter(name='gsyn_exc')[0],
               ylabel="gsyn excitatory (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    plot.Panel(gsyn_inh.segments[0].filter(name='gsyn_inh')[0],
               ylabel="gsyn inhibitory (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    title=title,
    annotations="Simulated with {}".format(p.name())
)
plt.show()
p.end()
print "\n job done"
