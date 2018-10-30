import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 0.1
p.setup(timestep)  # set simulation timestep (ms)
runtime = 10000

# Post-synapse population
new_i_offset = -50
num_intervals = 10
neuron_params = {
        'v': -88.1,
        'g_Na': 0.2,
        'E_Na': 30.0,
        'g_K': 1.85,
        'E_K': -90.0,
        'tau_m': 16,
        't_spike': 2,
        'i_offset': new_i_offset,
#         'v_thresh': 50,
#         'v_thresh_resting': 50
        }

pop_exc = p.Population(1,
                       p.extra_models.HillTononiNeuron(**neuron_params),
                       label="HT Neuron")

spike_times = [x + 50 for x in range(0, runtime, (runtime/num_intervals))]
# # Spike source to send spike via synapse
pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")

# Create projection
synapse = p.Projection(
    pop_src1, pop_exc, p.OneToOneConnector(),
    p.StaticSynapse(weight=1, delay=1), receptor_type="NMDA")

pop_exc.record("all")
for i in range(num_intervals):
    p.run(runtime/num_intervals)
    new_i_offset += 12.5
    pop_exc.set(i_offset=new_i_offset)

# pre_spikes = pop_src1.get_data('spikes')
exc_data = pop_exc.get_data()

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    # Panel(pre_spikes_slow.segments[0].spiketrains,
    # yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Threshold (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
    #       ylabel="gsyn excitatory (mV)",
    #       data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # Panel(exc_data.segments[0].spiketrains,
    #       yticks=True, markersize=0.2, xlim=(0, runtime)),
    )

plt.show()
p.end()
