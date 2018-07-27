import spynnaker8 as p
import numpy
import math
import glob
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

profiler_overhead = 0.000500
time_dict = {}
# time_dict['POP_TABLE_GET_FIRST'] = {}
# time_dict['POP_TABLE_GET_NEXT'] = {}
time_dict = {}

npc = [255] #range(1,255,10) # range(1,255,5) #[2**pow for pow in range(4,9)]
cores_contending = [1] #  [2**pow for pow in range(5)]
probs = [0.01, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
         0.5, 0.55, 0.6, 0.65,  0.7, 0.75,  0.8, 0.85,  0.9, 0.95, 1]
if npc[-1] is 256:
    npc[-1] = 255

results = {}
time_dict = {}
for i in npc:
    time_dict[i]={}
    for j in cores_contending:
        time_dict[i][j]={}
        time_dict[i][j]["PROCESS_FIXED_SYNAPSES"] = {}


for i in npc:
    for j in cores_contending:
        for pr in probs:
            p.setup(1) # 1 for LIf; 0.1 for Izhikevich
            runtime = 1050 # Run for one second
            source_neurons = 1 # takes value: 1, 2, 100, 256
            target_neurons = i*j #cores_contending * npc # takes value: 1, 2, 100, 256
            recording = False

            ## Create target population of neurons - comment as appropriate
            target_pop = p.Population(target_neurons, p.IF_curr_exp(),  label="test")
            # target_pop = p.Population(target_neurons, p.Izhikevich(),  label="test")

            # Partition to single neuron per core
            p.set_number_of_neurons_per_core(p.IF_curr_exp, i)

            ## Create source population of neurons
            spike_times = range(10,1010,10)
            source_pop = p.Population(source_neurons, p.SpikeSourceArray,
                                    {'spike_times': spike_times}, label="src1")


            # Connect neurons all-to-all
            a2a_proj = p.Projection(
                source_pop, target_pop,
                p.FixedProbabilityConnector(p_connect=1*pr
                                            ),
    #             p.AllToAllConnector(),
                p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

            # Set recording and run
            if recording:
                source_pop.record("all")
                target_pop.record("all")

            p.run(runtime)


            # Read profiler log to extract spike time
            path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/*0_0*3*"
            diffs = []
            # Process iobuf
            file = open(glob.glob(path)[1])
            for line in file.readlines():
                if line.__contains__("Diff"):
                    diffs.append(float(line.split(" ")[-1].split("\n")[0]))

            file.close()


            file = open(glob.glob(path)[0])
            for line in file.readlines():
                if line.__contains__("Total_pre_synaptic_events"):
                    pre_synaptic_events = line.split(">")[-2].split("<")[0]

#             print pre_synaptic_events
            results[pr] = (numpy.mean(diffs), pre_synaptic_events)

#         print "min: {}".format(min(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))
#         print "max: {}".format(max(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))
#         print "mean: {}".format(numpy.mean(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))


p.end()

for i in probs:
    print results[i][0], results[i][1]

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






