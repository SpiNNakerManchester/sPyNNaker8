import spynnaker8 as p
import matplotlib.pyplot as plt
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import RandomDistribution, NumpyRNG

'''
Paper Model Parameters
cell_rows = 132
cell_cols = 112
timestep = 1
rest_pot = -65mV
reset_pot = -67mV
thres_pot = -63mV
membrane_time_constant = 10ms
membrane_resistance = 10 ohm
refractory_period = 5ms
input_curr = 2.4mA
vel_curr = 0.175mA
orientation_pref_shift = 2
syn_weight = -0.6mV
syn_delay = 5*rand()
'''

p.setup(1)  # simulation timestep (ms)
runtime = 500

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -65,
    "v_rest": -65,
    "i_offset": 1,  # DC input
    "i_vel_drive": 0,
    "tau_m": 20,  # membrane time constant
    "tau_refrac": 1,
}

rng = NumpyRNG(seed=41, parallel_safe=True)
v_init = RandomDistribution('uniform', (-65, -55), rng)
pop_exc = p.Population(1,
                       p.extra_models.GridCell(**neuron_params),
                       cellparams=None,
                       initial_values={'v': v_init},
                       structure=None,
                       label="Grid cells"
                       )

pop_exc.record("all")
p.run(runtime)

exc_data = pop_exc.get_data()
firing_rate = len(exc_data.segments[0].spiketrains[0]) * (1000/runtime)
print("Mean spike count=" + str(pop_exc.mean_spike_count(gather=True)))

# Plot
F = Figure(
    # plot data for postsynaptic neuron
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
          yticks=True, xticks=True, markersize=2, xlim=(0, runtime)
          ),
)

plt.show()
p.end()

print("Firing rate=" + str(firing_rate) + "Hz")
print("i_offset=" + str(neuron_params['i_offset']) + "nA")
print("tau_refrac=" + str(neuron_params['tau_refrac']) + "ms")
print("tau_m=" + str(neuron_params['tau_m']) + "ms")
