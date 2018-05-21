import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1) # 1 for LIf; 0.1 for Izhikevich
runtime = 1000 # Run for one second
source_neurons = 1 # takes value: 1, 2, 100, 256
target_neurons = 1 # takes value: 1, 2, 100, 256
recording = True

## Create source population of neurons
spike_times = [10]
source_pop = p.Population(source_neurons, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")

## Create target population of neurons - comment as appropriate
target_pop = p.Population(target_neurons, p.IF_curr_exp(),  label="test")
# target_pop = p.Population(target_neurons, p.Izhikevich(),  label="test")

# Partition to single neuron per core
p.set_number_of_neurons_per_core(p.IF_curr_exp, 1)

# Connect neurons all-to-all
a2a_proj = p.Projection(
    source_pop, target_pop, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

# Set recording and run
if recording:
    source_pop.record("all")
    target_pop.record("all")

p.run(runtime)

# Extract output data
if recording:
    source_data = source_pop.get_data()
    target_data = target_pop.get_data()

    # Plot
    Figure(
        # raster plot of neuron spike times
        Panel(source_data.segments[0].spiketrains,
              yticks=True, markersize=0.2, xlim=(0, runtime)),
        Panel(target_data.segments[0].spiketrains,
              yticks=True, markersize=0.2, xlim=(0, runtime))
    )
    plt.show()

p.end()


