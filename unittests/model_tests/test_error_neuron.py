import spynnaker8 as pyNN
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

simtime = 1000

timestep = 1
pyNN.setup(timestep)  # simulation timestep (ms)

error_neuron = pyNN.Population(1,
                               pyNN.extra_models.ErrorNeuron(**{"i_offset": 1}),
                               label="label_activated_error_neuron")


label_src = pyNN.Population(10, pyNN.SpikeSourcePoisson(**{"rate":50}),
                            label="label_source" )


label_proj = pyNN.Projection(label_src, error_neuron,
                             pyNN.AllToAllConnector(),
                             pyNN.StaticSynapse(weight=0.05, delay=timestep),
                             receptor_type="label")

error_neuron.record('all')
label_src.record('spikes')

# Run simulation - label present
pyNN.run(simtime/3)

# Stop label spikes
label_src.set(rate=0)
pyNN.run(simtime/3)

# Start label spikes again
label_src.set(rate=50)
pyNN.run(simtime/3)

err_data = error_neuron.get_data()
label_data = label_src.get_data(['spikes'])

F = Figure(
    Panel(label_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, simtime)),
    Panel(err_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[error_neuron.label], yticks=True, xlim=(0, simtime)),
    Panel(err_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="Label Trace",
          data_labels=[error_neuron.label], yticks=True, xlim=(0, simtime)),
    Panel(err_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, simtime)))

plt.show()
pyNN.end()
print("job complete")