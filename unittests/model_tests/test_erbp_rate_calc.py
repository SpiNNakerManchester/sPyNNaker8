import spynnaker8 as p
import numpy
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 1
p.setup(timestep)  # simulation timestep (ms)
runtime = 10000

# Learning rule parameters
tau_err = 200.0
gamma = 0.3
w_err = 0.05
w_plastic = 0.5
dt = 16  # time difference of 15, +1 for a single timestep delay


# Hidden neuron population - i.e. postsynaptic population
neuron_params = {
    "v_thresh": 30.0,  # do not change - hard-coded in C for now
    "v_reset": 0.0,
    "v_rest": 0.0,
    "v": 20,
    "i_offset": 0,
    "tau_err": 1000,
    }  # DC input - to enable interesting p_j

pop_hidden = p.Population(1,  # number of neurons
                          p.extra_models.IFCurrExpERBP(**neuron_params),
                          label="ERBP Neuron")


poisson_src = p.Population(1, p.SpikeSourcePoisson(rate=10.0))

proj = p.Projection(
    poisson_src,
    pop_hidden,
    p.OneToOneConnector(),
    p.StaticSynapse(weight=10.0, delay=1),
    receptor_type='excitatory')


pop_hidden.record('all')

p.run(runtime/2)
poisson_src.set(rate=0)
p.run(runtime/2)

hidden_neuron_data = pop_hidden.get_data()

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(hidden_neuron_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, runtime)),
    Panel(hidden_neuron_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)
          ),
    Panel(hidden_neuron_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="target rate",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)),
    Panel(hidden_neuron_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="rate trace",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
        len(hidden_neuron_data.segments[0].spiketrains[0]))
        )

plt.show()
p.end()
