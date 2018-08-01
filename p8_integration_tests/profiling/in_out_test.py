import spynnaker8 as p
import numpy as np
import math
import glob
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


def _print_results(diffs, k):
    print "{}, {},  {},  {},  {}".format(
        k,
        round(np.mean(diffs[k]),0),
        min(diffs[k]),
        max(diffs[k]),
        np.std(diffs[k]))


runtime = 1010 # Run for one second
runtime = 100 # Run for one second
n_neurons = [1]
# n_neurons = [2, 16, 32, 64, 128, 255]
# n_neurons = [2, 255]
n_neurons.extend(range(2, 256, 4))
# n_neurons.extend(range(2, 150, 1))
n_neurons.append(255)
print n_neurons
#, 2, 4, 8, 16, 32, 64, 128, 255] # takes value 1, 2, 100, 256
source_neurons = 1
recording = False

alternating = False
grab = False

diffs = {}
mins = {}
maxs = {}

for n in n_neurons:

    p.setup(1) # 1 for LIF; 0.1 for Izhikevich

    ## Create population of neurons - comments as appropriate
    target_pop = p.Population(n, p.IF_curr_exp(),  label="test")
#     pop = p.Population(n, p.IF_cond_exp(),  label="test")
#     pop = p.Population(n, p.Izhikevich(),  label="test")
#     pop = p.Population(n, p.extra_models.Izhikevich_cond(),  label="test")

    # create spike source array to send spike
    spike_times = range(10,1010,10)
    spike_times = range(1,101,1)
    source_pop = p.Population(source_neurons, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="src1")

#     source_pop_2 = p.Population(source_neurons, p.SpikeSourceArray,
#                         {'spike_times': spike_times}, label="src2")

    # Connect neurons all-to-all
    a2a_proj = p.Projection(
    source_pop, target_pop, p.AllToAllConnector(),
    p.StaticSynapse(weight=0.01, delay=1), receptor_type="excitatory")

#     # Connect neurons all-to-all
#     a2a_proj_2 = p.Projection(
#     source_pop_2, target_pop, p.AllToAllConnector(),
#     p.StaticSynapse(weight=0.1, delay=5), receptor_type="excitatory")


    # Set recording and run
    if recording:
        pop.record("all")

    p.run(runtime)

    # Extract output data
    if recording:
        data = pop.get_data()


    # Read iobuf log to extract neuron update times
    path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/iobuf*0_0*3*"

    diffs[n] = []
    if alternating:
        diffs[-n] = []

    mins[n] = []
    maxs[n] = []

    # Process iobuf
    file = open(glob.glob(path)[0])
    for line in file.readlines():
        if line.__contains__("Diff"):
            if alternating:
                to_append = float(line.split(" ")[-1].split("\n")[0])
                if grab:
                    if to_append:
                        diffs[n].append(to_append)
                    grab = False
                else:
                    if to_append:
                        diffs[-n].append(to_append)
                    grab = True
            else:
                to_append = float(line.split(" ")[-1].split("\n")[0])
                if to_append:
                    diffs[n].append(to_append)

    file.close()

    print "Timing measurement output:"
    _print_results(diffs, n)
    if alternating:
        _print_results(diffs, -n)

    print "Length: {}".format(len(diffs[n]))

#     for d in diffs[n]:
#         print d

    p.end()


print "index 1"
for k in n_neurons:
    _print_results(diffs, k)

if alternating:
    print "index 0"
    for k in n_neurons:
        _print_results(diffs, -k)




