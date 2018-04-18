import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import glob
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Test creating 100 single neuron populations (and hence 100 rows in the pop
# table). The simulation is then run 100 times, where only one source neuron
# fires in each test, but 100 times, allowing the average pop table lookup to
# be assessed

num_source_neurons = 31
profiler_overhead = 0.000350

time_dict = {}
time_dict['POP_TABLE_GET_FIRST'] = []
time_dict['POP_TABLE_GET_NEXT'] = []


for i in range(num_source_neurons):
    p.setup(1) # 1 for LIf; 0.1 for Izhikevich
    runtime = 1011 # Run for one second
    source_neurons = 1 # takes value: 1, 2, 100, 256
    target_neurons = 1 # takes value: 1, 2, 100, 256
    recording = False

    source_pops = []

    ## Create source population of neurons
    for pop in range(num_source_neurons):
        spike_times = []
        if pop is i:
            spike_times = range(10,1010,10)
        source_pops.append(p.Population(source_neurons, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1"))

    ## Create target population of neurons - comment as appropriate
    target_pop = p.Population(target_neurons, p.IF_curr_exp(),  label="test")
    # target_pop = p.Population(target_neurons, p.Izhikevich(),  label="test")

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
    path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/*profile*"

    file = open(glob.glob(path)[0], 'r')

    for line in file.readlines():
        # print line
        if line.startswith('POP_TABLE_GET_NEXT'):
            time_dict['POP_TABLE_GET_NEXT'].append(float(line.split()[2]) - profiler_overhead)
        if line.startswith('POP_TABLE_GET_FIRST'):
            time_dict['POP_TABLE_GET_FIRST'].append(float(line.split()[2]) - profiler_overhead)

    file.close()
    p.end()


# printing 'get first' times
for t in time_dict['POP_TABLE_GET_FIRST']:
    print t



print "\n"
# printing 'get next' times
for t in time_dict['POP_TABLE_GET_NEXT']:
    print t

l = list(set(time_dict['POP_TABLE_GET_FIRST']))
l.sort()

num_intervals = int(math.ceil(math.log(num_source_neurons,2)))
print numpy.histogram(time_dict['POP_TABLE_GET_FIRST'], bins=num_intervals)[0], \
        l
plt.hist(time_dict['POP_TABLE_GET_FIRST'], num_intervals)
plt.show()
