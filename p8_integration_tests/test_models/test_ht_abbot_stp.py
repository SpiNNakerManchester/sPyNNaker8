import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

timestep = 1
p.setup(timestep)
runtime = 2000
initial_run = 100  # to negate any initial conditions

# Facilitation STP parameters
STP_type_facil = 1  # 0 for depression; 1 for facilitation
f_facil = 0.4
P_baseline_facil = 0.1
tau_P_facil = 50

# Depression STP parameters
STP_type_depress = 0  # 0 for depression; 1 for facilitation
f_depress = 0.6
P_baseline_depress = 1.0
tau_P_depress = 5

# Common parameters
baseline_weight = 0.33

spike_times = [1, 11, 21, 31, 41, 51, 61, 300]
facil_spike_times = [initial_run + i for i in spike_times]
depress_spike_times = [10*initial_run + i for i in spike_times]

# Spike source to send spike via plastic synapse
facil_src = p.Population(1, p.SpikeSourceArray,
                         {'spike_times': facil_spike_times}, label="facil src")
depress_src = p.Population(1, p.SpikeSourceArray,
                           {'spike_times': depress_spike_times},
                           label="depress src")

# Post-synapse population
pop_exc = p.Population(1, p.extra_models.HillTononiNeuron(),  label="test")

# Create synapse dynamics
facil_syn_plas = p.STDPMechanism(
        timing_dependence=p.AbbotSTP(
            STP_type_facil, f_facil, P_baseline_facil, tau_P_facil),
        weight_dependence=p.STPOnlyWeightDependence(),
        weight=baseline_weight, delay=timestep)

depress_syn_plas = p.STDPMechanism(
        timing_dependence=p.AbbotSTP(
            STP_type_depress, f_depress, P_baseline_depress, tau_P_depress),
        weight_dependence=p.STPOnlyWeightDependence(),
        weight=baseline_weight, delay=timestep)

# Create projections
synapse = p.Projection(facil_src,
                       pop_exc,
                       p.FromListConnector([(0,0,0.3,1)]),
                       synapse_type=facil_syn_plas,
                       receptor_type='NMDA')

synapse = p.Projection(depress_src,
                       pop_exc,
                       p.OneToOneConnector(),
                       synapse_type=depress_syn_plas,
                       receptor_type='NMDA')

facil_src.record('all')
depress_src.record('all')
pop_exc.record("all")
p.run(initial_run + runtime)
weights = []

weights.append(synapse.get('weight', 'list',
                           with_address=False)[0])

pre_spikes_slow = facil_src.get_data('spikes')
exc_data = pop_exc.get_data()

print "Post-synaptic neuron firing frequency: {} Hz".format(
    len(exc_data.segments[0].spiketrains[0]))

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(pre_spikes_slow.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(exc_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    Panel(exc_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mA)",
          data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # Panel(exc_data.segments[0].filter(name='gsyn_inh')[0],
    #       ylabel="gsyn inhibitory (mV)",
    #       data_labels=[pop_exc.label], yticks=True, xlim=(0, runtime)),
    # Panel(exc_data.segments[0].spiketrains,
    #       yticks=True, markersize=0.2, xlim=(0, runtime)),
    annotations="Post-synaptic neuron firing frequency: {} Hz".format(
        len(exc_data.segments[0].spiketrains[0]))
)
plt.show()
p.end()
