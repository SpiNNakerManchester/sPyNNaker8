import spynnaker8 as p
from pyNN.random import RandomDistribution
import numpy as np
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt


timestep = 1
runtime = 1000
initial_run = 100  # to negate any initial conditions

currents = np.linspace(0.2,0.8,21)
frequencies = []

for offset in currents:

    p.setup(timestep)

    # test-neuron
    pop_exc = p.Population(1,
                           p.IF_curr_exp(tau_m=30,
                                         #v_rest=0, v_reset=0, v_thresh=15,
                                         tau_syn_E=3, tau_syn_I=3, tau_refrac=3,
                                         i_offset = offset),
                           label="test")

    pop_exc.initialize(v=13.5)

    pop_exc.record("all")
    p.run(initial_run + runtime)

    exc_data = pop_exc.get_data()

    # print "neuron firing frequency: {} Hz".format(
    #      len(exc_data.segments[0].spiketrains[0]))

    frequencies.append(len(exc_data.segments[0].spiketrains[0]))

    # Plot
    # Figure(
    #     # plot data for postsynaptic neuron
    #     Panel(exc_data.segments[0].filter(name='v')[0],
    #           ylabel="Membrane potential (mV)",
    #           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # #     Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
    # #           ylabel="gsyn excitatory (mA)",
    # #           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # #     Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
    # #           ylabel="gsyn inhibitory (mV)",
    # #           data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # #     Panel(exc_data.segments[0].spiketrains,
    # #           yticks=True, markersize=0.2, xlim=(0, runtime)),
    #     # raster plot of the neuron spike times
    #     Panel(exc_data.segments[0].spiketrains,
    #           yticks=True, markersize=0.2, xlim=(0, runtime)),
    #     annotations="neuron firing frequency: {} Hz".format(
    #     len(exc_data.segments[0].spiketrains[0]))
    # )
    # plt.show()
    # p.end()


plt.figure(1)
plt.plot(currents, frequencies)
plt.xlabel('offset current (A)')
plt.ylabel('frequency (Hy)')
plt.show()

