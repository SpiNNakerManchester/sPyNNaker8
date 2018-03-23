import spynnaker8 as p
from pyNN.random import RandomDistribution
import pylab
import numpy
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


# Neuron populations
pop_exc = p.Population(
            n_exc,
            p.IF_curr_exp(tau_m=30,
#                           v_rest=13.5, v_reset=13.5, v_thresh=15,
                          tau_syn_E=3, tau_syn_I=3, tau_refrac=3,
#                          i_offset = 0.5),
                          #i_offset=RandomDistribution("uniform", low=0.35, high=0.6)),
                          i_offset=RandomDistribution("uniform", low=0.494, high=0.503)),
            label="Excitatory")
pop_inh = p.Population(
            n_inh,
            p.IF_curr_exp(tau_m=30,
#                           v_rest=13.5, v_reset=13.5, v_thresh=15,
                          tau_syn_E=3, tau_syn_I=3, tau_refrac=2,
#                          i_offset = 0.5),
                          #i_offset=RandomDistribution("uniform", low=0.35, high=0.6)),
                          i_offset=RandomDistribution("uniform", low=0.494, high=0.503)),
            label="Inhibitory")


p.set_number_of_neurons_per_core(p.IF_curr_exp, 32)

# Create synapse dynamics
depress_syn_plas_ee = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
#                               0, 0.5, 1.0, 800),
                                0, 0.5, 1.0, 800), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=1.8, delay=timestep)
depress_syn_plas_ei = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
#                               0, 0.5, 1.0, 800),
                                0, 0.5, 1.0, 800), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=5.4, delay=timestep)
depress_syn_plas_ii = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
#                               1, 0.04, 0.1, 1000),
                                1, 0.04, 0.1, 1000), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=7.2, delay=timestep)
depress_syn_plas_ie = p.STDPMechanism(
                            timing_dependence=p.AbbotSTP(
#                               1, 0.04, 0.1, 1000),
                                1, 0.04, 0.1, 1000), # STP_type, f, P_baseline, tau_P
                            weight_dependence=p.STPOnlyWeightDependence(),
                            weight=7.2, delay=timestep)



#conn = p.FixedProbabilityConnector(0.1)
conn = p.FixedProbabilityConnector(0.1)

p.Projection(
    pop_exc, pop_exc, conn, depress_syn_plas_ee, receptor_type="excitatory")
p.Projection(
    pop_exc, pop_inh, conn, depress_syn_plas_ei, receptor_type="excitatory")
p.Projection(
    pop_inh, pop_inh, conn, depress_syn_plas_ii, receptor_type="inhibitory")
p.Projection(
    pop_inh, pop_exc, conn, depress_syn_plas_ie, receptor_type="inhibitory")




#pop_exc.initialize(v=RandomDistribution("uniform", low=0, high=15))
#pop_inh.initialize(v=RandomDistribution("uniform", low=0, high=15))
pop_exc.initialize(v=RandomDistribution("uniform", low=-65, high=-50))
pop_inh.initialize(v=RandomDistribution("uniform", low=-65, high=-50))


pop_exc.record("spikes")

p.run(initial_run + runtime)


data = pop_exc.get_data("spikes")
end_time = p.get_current_time()

#p.end()


Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(data.segments[0].spiketrains,
          yticks=True, markersize=2.0, xlim=(0, end_time)),
    title="network simulation",
    annotations="Simulated with {}".format(p.name())
)
pylab.show()

