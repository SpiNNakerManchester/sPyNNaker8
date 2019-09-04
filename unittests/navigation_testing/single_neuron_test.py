import matplotlib.pyplot as plt
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.utility.plotting import Figure, Panel

import spynnaker8 as p

p.setup(1)  # simulation timestep (ms)
runtime = 1000

# Post-synapse population
neuron_params = {
    "v_thresh": -50.0,
    "v_reset": -65.0,
    "v_rest": -65.0,
    "i_offset": 0.758,
    "tau_m": 20,
    "tau_refrac": 1.0,
}

rng = NumpyRNG(seed=41, parallel_safe=True)
v_init = RandomDistribution('uniform', (-65, -55), rng)
pop_exc = p.Population(10,
                       p.IF_curr_exp(**neuron_params),
                       cellparams=None,
                       initial_values={'v': -65.0},
                       structure=None,
                       label="Grid cell"
                       )

pop_exc.record("all")
p.run(runtime)

exc_data = pop_exc.get_data()
print("Mean spike count=" + str(pop_exc.mean_spike_count(gather=True)) + "Hz")

# Plot
F = Figure(
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="excitatory synaptic conduction (uS)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="inhibitory synaptic conduction (uS)",
          xlabel="Time (ms)",
          data_labels=[pop_exc.label], yticks=True, xticks=True, xlim=(0, runtime)
          ),
    Panel(exc_data.segments[0].spiketrains,
          xlabel="Time (ms)",
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()

print("i_offset=" + str(neuron_params['i_offset']) + "nA")
