"""
Synfirechain-like example
"""
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

runtime = 5000
p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0,
        n_chips_required=(48 * 2) + 1)

nNeurons = 200  # number of neurons in each population
p.set_number_of_neurons_per_core(p.IF_curr_exp, nNeurons / 2)

cell_params_lif = {
    'cm': 0.25,
    'i_offset': 0.0,
    'tau_m': 20.0,
    'tau_refrac': 2.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 5.0,
    'v_reset': -70.0,
    'v_rest': -65.0,
    'v_thresh': -50.0}

populations = list()
projections = list()

weight_to_spike = 2.0
delay = 4

loopConnections = list()
for i in range(0, nNeurons - 1):
    singleConnection = ((i, i + 1, weight_to_spike, delay))
    loopConnections.append(singleConnection)

injectionConnection = [(0, 0)]
joiner_connection = [(nNeurons - 1, 0)]
spikeArray = {'spike_times': [[0]]}
locs = [(0, 0), (5, 5), (10, 6), (2, 10), (9, 1), (4, 8)]
for index in range(0, len(locs)):
    populations.append(
        p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif),
                     label='pop_{}'.format(index)))

for pop, loc in zip(populations, locs):
    pop.set_mapping_constraint({'x': loc[0], 'y': loc[1]})

for index in range(0, len(populations) - 1):
    projections.append(p.Projection(
        populations[index], populations[index+1],
        p.FromListConnector(joiner_connection),
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))

for pop in populations:
    projections.append(p.Projection(
        pop, pop, p.FromListConnector(loopConnections),
        p.StaticSynapse(weight=weight_to_spike, delay=delay)))

ssa = p.Population(1, p.SpikeSourceArray(**spikeArray), label='inputSpikes_1')
projections.append(p.Projection(
    ssa, populations[0], p.FromListConnector(injectionConnection),
    p.StaticSynapse(weight=weight_to_spike, delay=1)))

for pop in populations:
    pop.record(['v', 'gsyn_exc', 'gsyn_inh', 'spikes'])

p.run(runtime)

# get data (could be done as one, but can be done bit by bit as well)
v = populations[0].get_data('v')
gsyn_exc = populations[0].get_data('gsyn_exc')
gsyn_inh = populations[0].get_data('gsyn_inh')
spikes = list()
for pop in populations:
    spikes.append(pop.get_data('spikes'))

panels = list()
for spike in spikes:
    panels.append(
        Panel(spike.segments[0].spiketrains, yticks=True, markersize=0.2,
              xlim=(0, runtime)))
Figure(
    # raster plot of the presynaptic neuron spike times
    *panels,
    title="Simple synfire chain example",
    annotations="Simulated with {}".format(p.name()))
plt.show()

p.end()
