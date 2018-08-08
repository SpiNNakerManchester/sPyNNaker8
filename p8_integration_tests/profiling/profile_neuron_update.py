import spynnaker8 as p
import numpy as np
import math
import glob
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


runtime = 100 # Run for one second
n_neurons = [3] #[1, 2, 4, 8, 16, 32, 64, 128, 255] # takes value 1, 2, 100, 256
recording = True

for n in n_neurons:

    p.setup(1) # 1 for LIF; 0.1 for Izhikevich

    ## Create population of neurons - comments as appropriate
    pop = p.Population(n, p.IF_curr_exp(),  label="test")
#     pop = p.Population(n, p.IF_cond_exp(),  label="test")
#     pop = p.Population(n, p.Izhikevich(),  label="test")
#     pop = p.Population(n, p.extra_models.Izhikevich_cond(),  label="test")

#     pop.set(i_offset=5)

    # Set recording and run
    if recording:
        pop.record("all")

    p.run(runtime)

    # Extract output data
    if recording:
        data = pop.get_data()


    # Read iobuf log to extract neuron update times
    path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/iobuf*0_0*3*"
    diffs = {}
    mins = {}
    maxs = {}
    diffs[n] = []
    mins[n] = []
    maxs[n] = []

    # Process iobuf
    file = open(glob.glob(path)[0])
    for line in file.readlines():
        if line.__contains__("Diff"):
            if float(line.split(" ")[-1].split("\n")[0]):
                diffs[n].append(float(line.split(" ")[-1].split("\n")[0]))

    file.close()

    print "Timing measurement output:"
    print "{},  {},  {},  {}".format(round(np.mean(diffs[n]),0), min(diffs[n]), max(diffs[n]), np.std(diffs[n]))



    p.end()


