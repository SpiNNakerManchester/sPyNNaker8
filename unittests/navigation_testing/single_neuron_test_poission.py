import matplotlib.pyplot as plt
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.utility.plotting import Figure, Panel

import spynnaker8 as p

p.setup(1)  # simulation timestep (ms)
runtime = 1000

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 0,  # DC input
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1,
}

rng = NumpyRNG(seed=41, parallel_safe=True)
v_init = RandomDistribution('uniform', (-65, -55), rng)
pop_exc = p.Population(1,
                       p.IF_curr_exp(**neuron_params),
                       cellparams=None,
                       initial_values={'v': -65},
                       structure=None,
                       label="Grid cell"
                       )

pop_input = p.Population(1,
                         p.SpikeSourcePoisson(
                             rate=50, start=0, duration=runtime),
                         label="Poisson input velocity cells")

proj_input = p.Projection(pop_input, pop_exc,
                          p.OneToOneConnector(),
                          receptor_type="excitatory",
                          synapse_type=p.StaticSynapse(weight=0.25, delay=1.0),
                          label="Velocity input cells excitatory connections to appropriate grid cells"
                          )

pop_exc.record("all")
pop_input.record("all")
p.run(runtime)

exc_data = pop_exc.get_data()
print("Max v=" + str(max(exc_data.segments[0].filter(name='v')[0])))
gsyn_exc = map(float, exc_data.segments[0].filter(name='gsyn_exc')[0])
print("Max gsyn_exc=" + str(max(gsyn_exc)))

gsyn_exc_filtered = filter(lambda a: a != 0, gsyn_exc)  # Remove 0s in gsyn_exc
print("Avg gsyn_exc=" + str(sum(gsyn_exc_filtered) / len(gsyn_exc_filtered)))
print("Avg gsyn_exc=" + str(sum(gsyn_exc) / len(gsyn_exc)))
print("Mean spike count=" + str(pop_exc.mean_spike_count(gather=True)) + "Hz")

# Plot
F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
)
plt.show()

F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="excitatory synaptic conduction (nA)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
)
plt.show()

F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
    Panel(pop_input.get_data().segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)
plt.show()

F = Figure(
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="excitatory synaptic conduction (nA)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    # Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
    #       ylabel="inhibitory synaptic conduction (mV)",
    #       xlabel="Time (ms)",
    #       data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
    #       ),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
    Panel(pop_input.get_data().segments[0].spiketrains,
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()

print("i_offset=" + str(neuron_params['i_offset']) + "nA")
