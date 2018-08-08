import spynnaker8 as p
import numpy as np
import math
import glob
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as pltx
from pyNN.random import NumpyRNG, RandomDistribution


def _print_results(diffs, k):
    print "{}, {},  {},  {},  {}".format(
        k,
        round(np.mean(diffs[k]),0),
        min(diffs[k]),
        max(diffs[k]),
        np.std(diffs[k]))


diffs = {}
mins = {}
maxs = {}
alternating = False
grab = False

neurons_per_core = 128
n_neurons = [neurons_per_core]
p_connect = [0.9] # [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

window = 1
low_spikes_per_tick = [51]
# low_spikes_per_tick = [135, 105, 90 ]
# low_spikes_per_tick = [90, 60, 48, 38, 30, 25, 22, 20, 16, 15] # 255 NPC
# low_spikes_per_tick = [165, 145, 127, 112, 102, 93, 85, 78, 72, 67] # 64 NPC
# low_spikes_per_tick = [200, 190, 177, 167, 150, 130, 123, 117, 111, 105] # 32 NPC
# low_spikes_per_tick = [210, 210, 200, 195, 180, 180, 175, 170, 165, 155 ] # 16 NPC
# low_spikes_per_tick = [220, 220, 210, 205, 205, 205, 200, 195, 190, 185] # 8 NPC

high_spikes_per_tick = [l + window for l in low_spikes_per_tick]

for x in range(len(p_connect)):
        p.setup(1) # set simulation timestep (ms)
        runtime = 100
        spike_times = range(1, runtime+1, 1)

        rngseed = 98766987
        rng = NumpyRNG(seed=rngseed, parallel_safe=True)
        uniformDistr = RandomDistribution('uniform', [-65, 20], rng=rng)

        # Post-synapse population
        neuron_params = {
            "v_thresh": 50,
            'v_init': uniformDistr,
        #     "v_reset": -70,
            "i_offset": -0.750,
                         }

        # Spike source to send spike via synapse
        pop_srcs = []
        pop_excs = []
        synapses = []


        source_sizes = range(low_spikes_per_tick[0], high_spikes_per_tick[0])

        for i in range(len(source_sizes)):
            pop_excs.append(p.Population(
                neurons_per_core, p.IF_curr_exp(**neuron_params),
                label="LIF Neuron")
                )

        for i in range(len(source_sizes)):
            pop_srcs.append(p.Population(source_sizes[i], p.SpikeSourceArray,
                                 {'spike_times': spike_times}, label="src2"))

            conn_list = []
            for j in range(source_sizes[i]):
                for k in range(
                    max(1, (int(p_connect[x] * neurons_per_core)))
                    ):
                    conn_list.append((j, k, 0.001, 5)
                        )

            print "source size: {}, conn_list: {}".format(source_sizes[i], len(conn_list))

            synapses.append(p.Projection(
                pop_srcs[i], pop_excs[i],
                p.FromListConnector(conn_list),
                p.StaticSynapse(weight=1, delay=5), receptor_type="excitatory"))

        pop_excs[0].record('spikes')

        p.run(runtime)



        print "neurons per core: {}, connection prob: {}".format(neurons_per_core, p_connect[x])

        # Read iobuf log to extract neuron update times
        path = p.globals_variables.get_simulator()._report_default_directory + "/provenance_data/iobuf*0_0*3*"
        n = x
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

            # Remove first and last two elements to limit timing measurements to subsequent spikes (not first or last)
        diffs[n].remove(diffs[n][0])
        diffs[n].remove(diffs[n][-1])
        diffs[n].remove(diffs[n][-1])

        print "Timing measurement output:"
        _print_results(diffs, n)
        if alternating:
            _print_results(diffs, -n)

        print "Length: {}".format(len(diffs[n]))

        for d in diffs[n]:
            print d

        spikes = pop_excs[0].get_data('spikes')
        # Plot
        F = Figure(
            # plot data for postsynaptic neuron
            Panel(spikes.segments[0].spiketrains,
                  yticks=True, markersize=2, xlim=(0, runtime))
                   )
        plt.show()

        p.end()


print "index 1"
for k in range(len(p_connect)):
    _print_results(diffs, k)

