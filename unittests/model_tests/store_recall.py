import spynnaker8 as p
from spinn_front_end_common.utility_models import (
ReverseIpTagMultiCastSource)
from spynnaker.pyNN.spynnaker_external_device_plugin_manager import (SpynnakerExternalDevicePluginManager)
from spynnaker.pyNN.utilities import constants
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np

# @staticmethod
def add_poisson_live_rate_control(poisson_population, controller):
    vertex = poisson_population._get_vertex
    SpynnakerExternalDevicePluginManager.add_edge(
        controller._get_vertex, vertex, constants.LIVE_POISSON_CONTROL_PARTITION_ID)


batches = 40
num_repeats = 10  # in a batch
cycle_time = 2047
timestep = 1
p.setup(timestep) # simulation timestep (ms)
runtime = num_repeats * cycle_time * batches


# # Post-synapse population
erbp_neuron_params = {
    "tau_err": 1000,
#     "tau_refrac": 50
    # "v_thresh": 30.0,  # do not change - hard-coded in C for now
    "v_reset": 0.0,
    'small_b': 0,
    'v_rest': 0.0,
    'v': 0,
    'tau_m': 20.0,
    'cm': 20, # Updated to suit tau_m of 20 and make membrane resistance 1
    'B': 10.0,
    'small_b_0': 10,
    'i_offset': 0,
    'tau_a': 1200,
    'beta': 1.7,
    'tau_refrac':3
    }

# Store recall parameters
prob_command = 1. / 6.
rate_on = 50
rate_off = 0
input_pop_size = 25

readout_neuron_params = {
    "v": 0,
    "v_thresh": 30, # controls firing rate of error neurons
    "poisson_pop_size": input_pop_size,
    }

tau_err = 20

init_weight = 0.2

p.set_number_of_neurons_per_core(p.extra_models.EPropAdaptive, 32)
p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 32)

w_in_rec_exc_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=init_weight, sigma=init_weight,
        low=0.0, high=2*init_weight)

w_in_rec_inh_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=init_weight, sigma=init_weight,
        low=0.0, high=2*init_weight)

w_rec_rec_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=init_weight, sigma=init_weight,
        low=0.0, high=2*init_weight)

w_rec_out = init_weight
w_rec_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_rec_out, sigma=w_rec_out,
        low=0.0, high=2*w_rec_out)

w_out_out = init_weight
w_out_out_dist = p.RandomDistribution(
        distribution='normal_clipped', mu=w_out_out, sigma=w_out_out,
        low=0.0, high=2*w_out_out)


###############################################################################
# Build Populations
###############################################################################

# Input population
pop_in = p.Population(4*input_pop_size,
                      p.SpikeSourcePoisson,
                      {'rate': rate_on},
                      label='pop_in')

# Recurrent population
pop_rec = p.Population(20,
                      p.extra_models.EPropAdaptive,
                      # {10 LIF, 10 adaptive},
                      label='pop_rec')

# Output population
pop_out = p.Population(3, # HARDCODED 3: One readout; one exc err, one inh err
                       p.extra_models.StoreRecallReadout(
                            **readout_neuron_params
                           ),  # Neuron model
                       label="pop_out" # identifier
                       )

###############################################################################
# Build Projections
###############################################################################

#######################################
# readout to poisson sources
#######################################

add_poisson_live_rate_control(poisson_population=pop_in, controller=pop_out)

# hidden_pop_timing_dependence=p.TimingDependenceERBP(
#         tau_plus=tau_err, A_plus=0.01, A_minus=0.01)
# hidden_pop_weight_dependence=p.WeightDependenceERBP(
#         w_min=0.0, w_max=1, reg_rate=0.1)
hidden_pop_timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=0.025, A_minus=0.025, is_readout=False)
hidden_pop_weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=3, reg_rate=0.0)

out_pop_timing_dependence=p.TimingDependenceERBP(
        tau_plus=tau_err, A_plus=0.025, A_minus=0.025, is_readout=True)
out_pop_weight_dependence=p.WeightDependenceERBP(
        w_min=0.0, w_max=3, reg_rate=0.0)

#######################################
# input to recurrent excitatory
#######################################

# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=hidden_pop_timing_dependence,
    weight_dependence=hidden_pop_weight_dependence,
    weight=w_in_rec_exc_dist,
    delay=timestep)

# Create excitatory projection from input to hidden neuron using learning rule
inp_rec_exc = p.Projection(
    pop_in,
    pop_rec,
    p.AllToAllConnector(),
#     p.StaticSynapse(weight=w_in_rec_exc_dist, delay=timestep),
    synapse_type=learning_rule,
    receptor_type="exc_err")

# input to recurrent inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=hidden_pop_timing_dependence,
    weight_dependence=hidden_pop_weight_dependence,
    weight=w_in_rec_inh_dist,
    delay=timestep)

# Create inhibitory projection from input to hidden neuron using learning rule
inp_rec_inh = p.Projection(
    pop_in,
    pop_rec,
    p.AllToAllConnector(),
#     p.StaticSynapse(weight=w_in_rec_inh_dist, delay=timestep),
    synapse_type=learning_rule,
    receptor_type="exc_err")


#######################################
# recurrent to recurrent
#######################################
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=hidden_pop_timing_dependence,
    weight_dependence=hidden_pop_weight_dependence,
    weight=w_rec_rec_dist,
    delay=timestep)

# Create excitatory recurrent projection
rec_rec_exc = p.Projection(
    pop_rec,
    pop_rec,
    p.FixedProbabilityConnector(1.0),
    synapse_type=learning_rule,
    receptor_type="excitatory")

# input to recurrent inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=hidden_pop_timing_dependence,
    weight_dependence=hidden_pop_weight_dependence,
    weight=w_rec_rec_dist,
    delay=timestep)

# Create inhibitory recurrent projection from input to hidden neuron using
# learning rule
rec_rec_inh = p.Projection(
    pop_rec,
    pop_rec,
    p.FixedProbabilityConnector(1.0),
    synapse_type=learning_rule,
    receptor_type="inhibitory")

#######################################
# recurrent to output
#######################################

# Only connect to neuron '0' of readout population
# rand_out_w.next(),
conn_list_exc = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]
conn_list_inh = [[x, 0, w_rec_out_dist.next(), 1] for x in range(100)]

for i in range(0,100,2):
    conn_list_exc[i][2] = 0
    conn_list_inh[i+1][2] = 0


# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=out_pop_timing_dependence,
    weight_dependence=out_pop_weight_dependence,
    weight=w_rec_out_dist,
    delay=timestep)

# Create excitatory recurrent to out projection
rec_out_exc = p.Projection(
    pop_rec,
    pop_out,
    p.FromListConnector(conn_list_exc),
#     synapse_type=p.StaticSynapse(weight=0.1, delay=1),
    synapse_type=learning_rule,
    receptor_type="excitatory")

# recurrent to out inhibitory
# Define learning rule object
learning_rule = p.STDPMechanism(
    timing_dependence=out_pop_timing_dependence,
    weight_dependence=out_pop_weight_dependence,
    weight=w_rec_out_dist,
    delay=timestep)

# Create inhibitory recurrent projection from recurrent to hidden neuron using
# learning rule
rec_out_inh = p.Projection(
    pop_rec,
    pop_out,
    p.FromListConnector(conn_list_inh),
#     p.StaticSynapse(weight=0.1, delay=1),
    synapse_type=learning_rule,
    receptor_type="inhibitory")

#######################################
# Feedback connections
#######################################

# # Connect excitatory fb neuron (1) to all recurrent neurons
# # rand_out_w.next()
# exc_fb_rec_conn_list = [[1, x, 0.01*w_rec_out_dist.next(), 1] for x in range(100)]
# # Connect inhibitory fb neuron (2) to all recurrent neurons
# # rand_out_w.next()
# inh_fb_rec_conn_list = [[2, x, 0.01*w_rec_out_dist.next(), 1] for x in range(100)]
#
# fb_out_rec_exc = p.Projection(
#     pop_out, pop_rec, p.FromListConnector(exc_fb_rec_conn_list),
#     p.StaticSynapse(weight=10, delay=1), receptor_type="exc_err")
#
# fb_out_rec_inh = p.Projection(
#     pop_out, pop_rec, p.FromListConnector(inh_fb_rec_conn_list),
#     p.StaticSynapse(weight=10, delay=1), receptor_type="inh_err")


# Now to output layer to gate plasticity on output weights
# rand_out_w.next()
# rand_out_w.next()
exc_fb_out_conn_list  = [1, 0, w_out_out_dist.next(), 1]
inh_fb_out_conn_list  = [2, 0, w_out_out_dist.next(), 1]

fb_out_out_exc = p.Projection(
    pop_out, pop_out, p.FromListConnector([exc_fb_out_conn_list]),
    p.StaticSynapse(weight=0.5, delay=1), receptor_type="exc_err")

fb_out_out_inh = p.Projection(
    pop_out, pop_out, p.FromListConnector([inh_fb_out_conn_list]),
    p.StaticSynapse(weight=0.5, delay=1), receptor_type="inh_err")

###############################################################################
# Run Simulation
###############################################################################

pop_in.record('spikes')
pop_rec.record("spikes")
pop_out.record("all")


# p.run(runtime)
plot_start = 0
window =  num_repeats * cycle_time
plot_end = plot_start + window


for i in range(batches):

    print "run: {}".format(i)
    p.run(runtime/batches)

    in_spikes = pop_in.get_data('spikes')
    pop_rec_data = pop_rec.get_data('spikes')
    pop_out_data = pop_out.get_data()

    # Plot
    F = Figure(
#         # plot data for postsynaptic neuron
        Panel(in_spikes.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(plot_start, plot_end)),
        Panel(pop_rec_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='gsyn_exc')[0],
              ylabel="gsyn excitatory (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].filter(name='gsyn_inh')[0],
              ylabel="gsyn inhibitory (mV)",
              data_labels=[pop_out.label], yticks=True, xlim=(plot_start, plot_end)
              ),
        Panel(pop_out_data.segments[0].spiketrains,
              yticks=True, markersize=2, xlim=(plot_start, plot_end)),
        annotations="Batch: {}".format(i)
        )

    plt.pause(1)
#     plt.draw()

    plot_start = plot_end
    plot_end += window


p.end()


print "job done"

plt.show()