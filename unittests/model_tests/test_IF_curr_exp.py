import spynnaker8 as pyNN
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

simtime = 50

timestep = 1
pyNN.setup(timestep)  # simulation timestep (ms)

pop_error_pos = pyNN.Population(1,
                                pyNN.IF_curr_exp(),
                                label="IF_curr_exp_pop")

pop_error_pos.record('all')

# Run simulation
pyNN.run(simtime)

err_data = pop_error_pos.get_data()

F = Figure(
    Panel(err_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_error_pos.label], yticks=True, xlim=(0, simtime)),
    Panel(err_data.segments[0].spiketrains,
          yticks=True, markersize=2, xlim=(0, simtime)))
plt.show()
pyNN.end()
