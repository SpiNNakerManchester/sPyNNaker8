import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt



neurons_per_core = 255
p_connect = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

window = 20
# low_spikes_per_tick = [135, 105, 90 ]
low_spikes_per_tick = [90, 60, 48, 38, 30, 25, 22, 20, 16, 15] # 255 NPC
# low_spikes_per_tick = [165, 145, 127, 112, 102, 93, 85, 78, 72, 67] # 64 NPC
# low_spikes_per_tick = [200, 190, 177, 167, 150, 130, 123, 117, 111, 105] # 32 NPC
# low_spikes_per_tick = [210, 210, 200, 195, 180, 180, 175, 170, 165, 155 ] # 16 NPC
# low_spikes_per_tick = [220, 220, 210, 205, 205, 205, 200, 195, 190, 185] # 8 NPC

high_spikes_per_tick = [l + window for l in low_spikes_per_tick]

for x in range(len(low_spikes_per_tick)):
    p.setup(1) # set simulation timestep (ms)
    runtime = 10
    spike_times = [1]

    # Post-synapse population
    neuron_params = {
    #     "v_thresh": -50,
    #     "v_reset": -70,
        "i_offset": 0,
                     }

    # Spike source to send spike via synapse
    pop_srcs = []
    pop_excs = []
    synapses = []


    source_sizes = range(low_spikes_per_tick[x], high_spikes_per_tick[x])

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
                conn_list.append((j, k, 1.0, 5)
                    )

        print "source size: {}, conn_list: {}".format(source_sizes[i], len(conn_list))

        synapses.append(p.Projection(
            pop_srcs[i], pop_excs[i],
            p.FromListConnector(conn_list),
            p.StaticSynapse(weight=1.0, delay=5), receptor_type="excitatory"))


    p.run(runtime)

    print "neurons per core: {}, connection prob: {}".format(neurons_per_core, p_connect[x])







    p.end()


