import spynnaker8 as p
from pyNN.random import RandomDistribution
import pylab
import numpy as np
import math
from pyNN.utility.plotting import Figure, Panel
import unittest
import matplotlib.pyplot as plt


timestep = 1
p.setup(timestep)

#runtime = 4300
runtime = 5000
initial_run = 100  # to negate any initial conditions

n_neurons = 500
n_exc = int(round(n_neurons * 0.8))
n_inh = int(round(n_neurons * 0.2))


#current = 15
#current = RandomDistribution("uniform", low=14.625, high=15.375)
current = RandomDistribution("uniform", low=14.95, high=15.1)


# Neuron populations
pop_exc = p.Population(
            n_exc,
            p.IF_curr_exp(tau_m=30, cm=30,
                          v_rest=0, v_reset=13.5, v_thresh=15,
                          tau_syn_E=3, tau_syn_I=3, tau_refrac=3,
                          i_offset=current),
            label="Excitatory")
pop_inh = p.Population(
            n_inh,
            p.IF_curr_exp(tau_m=30, cm=30,
                          v_rest=0, v_reset=13.5, v_thresh=15,
                          tau_syn_E=3, tau_syn_I=3, tau_refrac=2,
                          i_offset=current),
            label="Inhibitory")


#p.set_number_of_neurons_per_core(p.IF_curr_exp, 32)

# Parameters for the synapses
Aee = 1.8
Aei = 5.4
Aii = 7.2
Aie = 7.2

Uee = 0.5
Uei = 0.5
Uii = 0.04
Uie = 0.04

tau_rec_ee = 800.0
tau_rec_ei = 800.0
#tau_rec_ii = 100.0
#tau_rec_ie = 100.0

tau_facil_ii = 1000.0
tau_facil_ie = 1000.0

synapse_delay = timestep
#synapse_delay = RandomDistribution("uniform", low=0, high=10)


# Create synapse dynamics
depress_syn_plas_ee = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
                                0, Uee, 1.0, tau_rec_ee), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=RandomDistribution("normal_clipped",
                                                      mu=Aee, sigma=Aee/2.0, high=2.0*Aee, low=0.2*Aee),
                            delay=synapse_delay)
depress_syn_plas_ei = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
                                0, Uei, 1.0, tau_rec_ei), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=RandomDistribution("normal_clipped",
                                                      mu=Aei, sigma=Aei/2.0, high=2.0*Aei, low=0.2*Aei),
                            delay=synapse_delay)
depress_syn_plas_ii = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
                                1, Uii, 0.1, tau_facil_ii), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=RandomDistribution("normal_clipped",
                                                      mu=Aii, sigma=Aii/2.0, high=2.0*Aii, low=0.2*Aii),
                            delay=synapse_delay)
depress_syn_plas_ie = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
                                1, Uie, 0.1, tau_facil_ie), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=RandomDistribution("normal_clipped",
                                                      mu=Aie, sigma=Aie/2.0, high=2.0*Aie, low=0.2*Aie),
                            delay=synapse_delay)



conn = p.FixedProbabilityConnector(0.1)

p.Projection(
    pop_exc, pop_exc, conn, depress_syn_plas_ee, receptor_type="excitatory")
p.Projection(
    pop_exc, pop_inh, conn, depress_syn_plas_ei, receptor_type="excitatory")
p.Projection(
    pop_inh, pop_inh, conn, depress_syn_plas_ii, receptor_type="inhibitory")
p.Projection(
    pop_inh, pop_exc, conn, depress_syn_plas_ie, receptor_type="inhibitory")




pop_exc.initialize(v=RandomDistribution("uniform", low=0, high=15))
pop_inh.initialize(v=RandomDistribution("uniform", low=0, high=15))


pop_exc.record("spikes")
pop_inh.record("spikes")

p.run(initial_run + runtime)


data_exc = pop_exc.get_data("spikes")
data_inh = pop_inh.get_data("spikes")

exc_spikes = data_exc.segments[0].spiketrains
inh_spikes = data_inh.segments[0].spiketrains

end_time = p.get_current_time()


# sort the neurons by spiking frequency
sorted_indices = []
for i in range(0, len(exc_spikes)):
    sorted_indices.append((len(exc_spikes[i]), i))
def getKey(item):
    return item[0]
sorted_indices = sorted(sorted_indices, key=getKey)
sorted_exc_spikes = []
for i in range(0, len(exc_spikes)):
    sorted_exc_spikes.append(exc_spikes[sorted_indices[i][1]])
for i in range(0, len(sorted_exc_spikes)):
    #sorted_exc_spikes[i].annotations['source_id'] = i
    sorted_exc_spikes[i].annotations['source_index'] = i

#p.end()


Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(exc_spikes,
          #sorted_exc_spikes,
          yticks=True, markersize=2.0, xlim=(0, end_time)),
#     Panel(inh_spikes,
#           #sorted_inh_spikes,
#           yticks=True, markersize=2.0, xlim=(0, end_time)),
    title="network simulation",
    annotations="Simulated with {}".format(p.name())
)
pylab.show()

