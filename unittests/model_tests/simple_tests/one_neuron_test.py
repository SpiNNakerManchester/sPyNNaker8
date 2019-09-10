import spynnaker8 as p
import numpy
import math
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # simulation timestep (ms)
runtime = 250

# Post-synapse population
neuron_params = {
    "u_thresh": -50,
    "u_reset": -70,
    "u_rest": -65,
    "i_offset": 0, # DC input
    "v": -65
    }

# spike_times = [float(x)/10 for x in range(1000)]
soma_spike_times = [40,50]
dendrite_spike_times = [80, 140, 160, 165, 168, 173, 180]
delays = 1.5


teacher_src = p.Population(1,
                           p.SpikeSourceArray,
                           {'spike_times': soma_spike_times},
                           label="teacher")
pop_src = p.Population(1,
                       p.SpikeSourceArray,
                       {'spike_times': dendrite_spike_times},
                       label="src")


two_comp_pop = p.Population(1, # number of neurons
                       p.extra_models.IFCurrExpTwoComp(
#                            **neuron_params
                           ),  # Neuron model
                       label="Two Comp LIF Neuron" # identifier
                       )


proj_exc_soma = p.Projection(teacher_src, two_comp_pop, p.OneToOneConnector(),
                    p.StaticSynapse(weight=1, delay=1), receptor_type="soma_exc")

# proj_inh_soma = p.Projection(teacher_src, two_comp_pop, p.OneToOneConnector(),
#                     p.StaticSynapse(weight=1, delay=10), receptor_type="soma_inh")

proj_exc_dendrite = p.Projection(pop_src, two_comp_pop, p.OneToOneConnector(),
                    p.StaticSynapse(weight=1.5, delay=1), receptor_type="dendrite_exc")

# proj_exc_dendrite = p.Projection(pop_src, two_comp_pop, p.OneToOneConnector(),
#                     p.StaticSynapse(weight=1, delay=10), receptor_type="dendrite_inh")

two_comp_pop.record("all")
teacher_src.record("spikes")
pop_src.record("spikes")
# two_comp_pop.record("spikes")

p.run(runtime)

teacher_data = teacher_src.get_data()
src_data = pop_src.get_data()
exc_data = two_comp_pop.get_data("all")
#
#
F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Soma potential (mV)",
          data_labels=[two_comp_pop.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="Dendrite potential (mV)",
          data_labels=[two_comp_pop.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Dendrite potential* (mV)",
          data_labels=[two_comp_pop.label], yticks=True, xlim=(0, runtime)
          ),
#     Panel(teacher_data.segments[0].spiketrains,
#           yticks=True, markersize=2, xlim=(0, runtime)
#           ),
#     Panel(src_data.segments[0].spiketrains,
#           yticks=True, markersize=2, xlim=(0, runtime)
#           ),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)
          ),
    )
#
p.end()
print "job done"
plt.show()



