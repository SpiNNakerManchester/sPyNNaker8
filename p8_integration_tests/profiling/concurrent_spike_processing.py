import spynnaker8 as p
import numpy
import math
import glob
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

profiler_overhead = 0.000350
time_dict = {}
# time_dict['POP_TABLE_GET_FIRST'] = {}
# time_dict['POP_TABLE_GET_NEXT'] = {}
time_dict = {}

npc = [256] #[2**pow for pow in range(4,9)]
cores_contending = [1]#  [2**pow for pow in range(5)]

if npc[-1] is 256:
    npc[-1] = 255

time_dict = {}
for i in npc:
    time_dict[i]={}
    for j in cores_contending:
        time_dict[i][j]={}
        time_dict[i][j]["DMA_SETUP_TO_CALLBACK"] = {}


for i in npc:
    for j in cores_contending:
        p.setup(1) # 1 for LIf; 0.1 for Izhikevich
        runtime = 1050 # Run for one second
        source_neurons = 1 # takes value: 1, 2, 100, 256
        target_neurons = i*j #cores_contending * npc # takes value: 1, 2, 100, 256
        recording = False



        ## Create target population of neurons - comment as appropriate
        target_pop = p.Population(target_neurons, p.IF_curr_exp(),  label="test")
        # target_pop = p.Population(target_neurons, p.Izhikevich(),  label="test")

        # Partition to single neuron per core
        p.set_number_of_neurons_per_core(p.IF_curr_exp, npc)

        ## Create source population of neurons
        spike_times = range(10,1010,10)
        source_pop = p.Population(source_neurons, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")


        # Connect neurons all-to-all
        a2a_proj = p.Projection(
            source_pop, target_pop,
            p.FixedProbabilityConnector(p_connect=0.1),
#             p.AllToAllConnector(),
            p.StaticSynapse(weight=0.1, delay=1), receptor_type="excitatory")

        # Set recording and run
        if recording:
            source_pop.record("all")
            target_pop.record("all")

        p.run(runtime)


        # Read profiler log to extract spike time
        path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/*profile*"

        for pa in glob.glob(path):
            file = open(pa, 'r')
            core_id = pa.split("_profile")[-2][-2:].split("_")[-1]
            print pa, core_id
            for line in file.readlines():
                # print line
#                 if line.startswith('POP_TABLE_GET_NEXT'):
#                     time_dict[npc[0]][cores_contending[0]]['POP_TABLE_GET_NEXT'][core_id] = float(line.split()[2]) - profiler_overhead
#
#                 if line.startswith('POP_TABLE_GET_FIRST'):
#                     time_dict['POP_TABLE_GET_FIRST'][core_id] = (float(line.split()[2]) - profiler_overhead)

                if line.startswith("DMA_SETUP_TO_CALLBACK"):
                    time_dict[i][j]["DMA_SETUP_TO_CALLBACK"][core_id] = (float(line.split()[2]) - profiler_overhead)


        # for k in time_dict['POP_TABLE_GET_NEXT'].keys():
        #     print k, time_dict['POP_TABLE_GET_NEXT'][k]
        #
        # for k in time_dict['POP_TABLE_GET_FIRST'].keys():
        #     print k, time_dict['POP_TABLE_GET_FIRST'][k]

#         for k in time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].keys():
#             print k, time_dict[i][j]['DMA_SETUP_TO_CALLBACK'][k]

#         print "min: {}".format(min(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))
#         print "max: {}".format(max(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))
#         print "mean: {}".format(numpy.mean(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()))


p.end()

for i in npc:
    for j in cores_contending:
        if len(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()) is not 0:
            print i, j, numpy.mean(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()), min(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values()), max(time_dict[i][j]['DMA_SETUP_TO_CALLBACK'].values())


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






