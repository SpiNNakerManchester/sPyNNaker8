import spynnaker8 as p
import numpy as  np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import glob
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


def _print_results(diffs, k):
    print "{}, {},  {},  {},  {}".format(
        k,
        round(np.mean(diffs[k]),0),
        min(diffs[k]),
        max(diffs[k]),
        np.std(diffs[k]))



# Test creating 100 single neuron populations (and hence 100 rows in the pop
# table). The simulation is then run 100 times, where only one source neuron
# fires in each test, but 100 times, allowing the average pop table lookup to
# be assessed


diffs = {}
mins = {}
maxs = {}

num_source_neurons = 1024


p.setup(1) # 1 for LIf; 0.1 for Izhikevich
runtime = 10*num_source_neurons + 10 # Run for one second
source_neurons = 1 # takes value: 1, 2, 100, 256
target_neurons = 1 # takes value: 1, 2, 100, 256
recording = False

## Create target population of neurons - comment as appropriate
target_pop = p.Population(target_neurons, p.IF_curr_exp(),  label="test")
# target_pop = p.Population(target_neurons, p.Izhikevich(),  label="test")

source_pops = []
offset = 0
## Create source population of neurons
for i in range(num_source_neurons):
#     for pop in range(num_source_neurons):
#         if pop is i:
    spike_times = [10 + offset]  #range(10,1010,10)
    source_pops.append(p.Population(source_neurons, p.SpikeSourceArray,
                            {'spike_times': spike_times}, label="src{}".format(i)))

    offset+=10

print spike_times

projs = []

# Connect neurons all-to-all
for source_pop in source_pops:
    projs.append(p.Projection(
        source_pop, target_pop, p.AllToAllConnector(),
        p.StaticSynapse(weight=0.01, delay=1),
                        receptor_type="excitatory"))

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

# Read profiler log to extract spike time
# Read iobuf log to extract neuron update times
path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/iobuf*0_0*_3*"
n = 0
diffs[n] = []


mins[n] = []
maxs[n] = []

# Process iobuf
file = open(glob.glob(path)[0])
for line in file.readlines():
    if line.__contains__("Diff"):
            to_append = float(line.split(" ")[-1].split("\n")[0])
            if to_append:
                diffs[n].append(to_append)

file.close()

# print "Timing measurement output:"
# _print_results(diffs, n)

print "Length: {}".format(len(diffs[n]))


p.end()


print "index 1"
for i in diffs[n]:
    print i
#     _print_results(diffs, k)





