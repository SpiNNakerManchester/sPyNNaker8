import pylab
import spynnaker8 as sim
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

sim.setup(timestep=1, min_delay=1.0, max_delay=4.0)

param_dict = {"V_compartment1":-45, "C_compartment1": 1943}

US_cell = sim.Population(1, sim.extra_models.IF_curr_comb_exp_US(**param_dict))



spike_sourceE = sim.Population(1000, sim.SpikeSourceArray(**{
    'spike_times': [5, 10, 15]}))
spike_sourceI = sim.Population(1, sim.SpikeSourceArray(**{
    'spike_times': [float(i) for i in range(155,166, 5)]}))

# Soma Projections
# sim.Projection(spike_sourceE, US_cell,
#                sim.OneToOneConnector(),
#                synapse_type=sim.StaticSynapse(weight=1.5, delay=2.0),
#                receptor_type='excitatory')
# sim.Projection(spike_sourceI, US_cell,
#                sim.OneToOneConnector(),
#                synapse_type=sim.StaticSynapse(weight=1.5, delay=4.0),
#                receptor_type='inhibitory')

# Dendrite projections
sim.Projection(spike_sourceE, US_cell,
               sim.AllToAllConnector(),
               synapse_type=sim.StaticSynapse(weight=0.5, delay=2.0),
               receptor_type='excitatory2')
sim.Projection(spike_sourceI, US_cell,
               sim.OneToOneConnector(),
               synapse_type=sim.StaticSynapse(weight=0.5, delay=4.0),
               receptor_type='inhibitory2')

US_cell.record('all')

runtime = 200.0

sim.run(runtime)
US_data = US_cell.get_data()

# Plot
Figure(
    # membrane potential of the postsynaptic neuron
    Panel(US_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[US_cell.label], yticks=True, xlim=(0, runtime)),
    Panel(US_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[US_cell.label], yticks=True, xlim=(0, runtime)),
    Panel(US_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[US_cell.label], yticks=True, xlim=(0, runtime)),
    title="Simple synfire chain example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()

sim.end()
pylab.show()
