import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 0.1
p.setup(timestep)  # set simulation timestep (ms)
runtime = 1500

neuron_params = {
    'v': -50
    }
patch_clamped_neuron = p.Population(1,
#                         p.IF_curr_exp(),
                    p.extra_models.PatchClamped(**neuron_params),
                    label="HT Neuron")

patch_clamped_neuron.record("all")

# patch_clamped_neuron.set(v=0)
p.run(runtime/3)
patch_clamped_neuron.set(v=10)
p.run(runtime/3)
patch_clamped_neuron.set(v=-50)
p.run(runtime/3)

# pre_spikes = pop_src1.get_data('spikes')
exc_data = patch_clamped_neuron.get_data()

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    # Panel(pre_spikes_slow.segments[0].spiketrains,
    # yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[patch_clamped_neuron.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Sum intrinsic currents (mV)",
          data_labels=[patch_clamped_neuron.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="Threshold (mV)",
          data_labels=[patch_clamped_neuron.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    )

plt.show()
p.end()
