import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # 1 for LIF; 0.1 for Izhikevich
runtime = 1000 # Run for one second
n_neurons = 1 # takes value 1, 2, 100, 256
recording = False



## Create population of neurons - comments as appropriate
pop = p.Population(n_neurons, p.IF_curr_exp(),  label="test")
# pop = p.Population(n_neurons, p.Izhikevich(),  label="test")

# Set recording and run
if recording:
    pop.record("all")

p.run(runtime)

# Extract output data
if recording:
    data = pop.get_data()

    # Plot
    Figure(
        # raster plot of neuron spike times
        Panel(data.segments[0].spiketrains,
              yticks=True, markersize=0.2, xlim=(0, runtime)),
    )
    plt.show()

p.end()


