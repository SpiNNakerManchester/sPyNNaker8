import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 0.1
p.setup(timestep)  # set simulation timestep (ms)
runtime = 300


base_potential = -70
clamped_potential = -20

neuron_params = {
    'v': base_potential,
    'm_K': 0.01
    }

patch_clamped_neuron = p.Population(1,
                                    p.extra_models.PatchClampedGenericSingleChannel(
                                        **neuron_params),
                                    label="Patch Clamped HT Neuron")

patch_clamped_neuron.record("all")

p.run(runtime/3)
patch_clamped_neuron.set(v=clamped_potential)
p.run(runtime/3)
patch_clamped_neuron.set(v=base_potential)
p.run(runtime/3)

exc_data = patch_clamped_neuron.get_data()

Figure(
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[patch_clamped_neuron.label], yticks=True,
          xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="I",
          data_labels=[patch_clamped_neuron.label], yticks=True,
          xlim=(0, runtime)))

plt.show()
p.end()
