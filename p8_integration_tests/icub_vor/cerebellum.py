import socket
import spynnaker8 as sim
import numpy as np
#import logging
import matplotlib.pyplot as plt

#from spynnaker8.utilities import DataHolder
from pacman.model.constraints.key_allocator_constraints import FixedKeyAndMaskConstraint
from pacman.model.graphs.application import ApplicationSpiNNakerLinkVertex
from pacman.model.routing_info import BaseKeyAndMask
from spinn_front_end_common.abstract_models.abstract_provides_n_keys_for_partition import AbstractProvidesNKeysForPartition
from spinn_front_end_common.abstract_models.abstract_provides_outgoing_partition_constraints import AbstractProvidesOutgoingPartitionConstraints
from spinn_utilities.overrides import overrides
from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import RandomDistribution, NumpyRNG

from spynnaker.pyNN.models.neuron.plasticity.stdp.common \
    import plasticity_helpers

# cerebellum with simulated input
RETINA_X_SIZE = 304
RETINA_Y_SIZE = 240
RETINA_BASE_KEY = 0x00000000
RETINA_MASK = 0xFF000000
RETINA_Y_BIT_SHIFT = 9

# class ICUBInputVertex(
#         ApplicationSpiNNakerLinkVertex,
#         # AbstractProvidesNKeysForPartition,
#          AbstractProvidesOutgoingPartitionConstraints):
#
#     def __init__(self, n_neurons, spinnaker_link_id, board_address=None,
#                  constraints=None, label=None):
#
#         ApplicationSpiNNakerLinkVertex.__init__(
#             self, n_neurons, spinnaker_link_id=spinnaker_link_id,
#             board_address=board_address, label=label, constraints=constraints)
#         #AbstractProvidesNKeysForPartition.__init__(self)
#         AbstractProvidesOutgoingPartitionConstraints.__init__(self)
#
# #    @overrides(AbstractProvidesNKeysForPartition.get_n_keys_for_partition)
# #    def get_n_keys_for_partition(self, partition, graph_mapper):
# #        return 1048576
#
#     @overrides(AbstractProvidesOutgoingPartitionConstraints.
#                get_outgoing_partition_constraints)
#     def get_outgoing_partition_constraints(self, partition):
#         return [FixedKeyAndMaskConstraint(
#             keys_and_masks=[BaseKeyAndMask(
#                 base_key=0, #upper part of the key
#                 mask=0xFFFFFC00)])]
#                 #keys, i.e. neuron addresses of the input population that sits in the ICUB vertex
#                 # this mask removes all spikes that have a "1" in the MSB and lets the spikes go only if the MSB are at "0"
#                 # it must have enough keys to host the input addressing space and the output (with the same keys)
# class ICUBInputVertexDataHolder(DataHolder):
#
#     def __init__(self, spinnaker_link_id, board_address=None,
#                  constraints=None, label=None):
#         DataHolder.__init__(
#             self, {"spinnaker_link_id": spinnaker_link_id,"board_address": board_address, "label": label})
#
#     @staticmethod
#     def build_model():
#         return ICUBInputVertex
# #logger = logging.getLogger(__name__)

# Synapsis parameters
gc_pc_weights = 0.005
mf_vn_weights = 0.001
pc_vn_weights = -0.00002
io_pc_weights = 0.0
mf_gc_weights = 0.0006
go_gc_weights = -0.0002
input_weights = 0.00025
mf_go_weights = 0.0006


# Network parameters
num_MF_neurons = 100
num_GC_neurons = 2000
num_GOC_neurons = 100
num_PC_neurons = 200
num_VN_neurons = 200
num_IO_neurons = 200

# Random distribution for synapses delays and weights (MF and GO)
delay_distr = RandomDistribution('uniform', (1.0, 10.0), rng=NumpyRNG(seed=85524))
weight_distr_MF = RandomDistribution('uniform', (mf_gc_weights*0.8, mf_gc_weights*1.2), rng=NumpyRNG(seed=85524))
weight_distr_GO = RandomDistribution('uniform', (go_gc_weights*0.8, go_gc_weights*1.2), rng=NumpyRNG(seed=24568))

# Post-synapse population
neuron_params = {
    "v_thresh": -50,
    "v_reset": -70,
    "v_rest": -65,
    "i_offset": 0 # DC input
                 }

# Learning parameters cos rule (MF to VN)
min_weight_c = 0
max_weight_c = 0.1
pot_alpha_c = 0.01 # this is alpha in the paper
beta_c = 11
sigma_c = 201
initial_weight_c = 0.005
initial_weight_c = 0.05
plastic_delay_c = 4

# Learning parameters sin rule (GrC to PC)
min_weight_s = 0
max_weight_s = 0.1
pot_alpha_s =0.01
t_peak_s =100
initial_weight_s = 0.05
plastic_delay_s = 4

sim.setup(timestep=1.)
#sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 255)

# set up input populations
# num_pxl = 304 * 240;
# retina_pop = sim.Population(1024, ICUBInputVertexDataHolder(spinnaker_link_id=0), label='pop_retina')

# Sensorial Activity: input activity from vestibulus (will come from the head IMU, now it is a test bench)
def sensorial_activity(pt):
    MAX_AMPLITUDE = 0.8
    RELATIVE_AMPLITUDE = 1.0
    _head_pos = []
    _head_vel = []

    i = np.arange(0,2,0.01)
    for t in i:
        desired_speed=-np.cos(t*2*np.pi)*MAX_AMPLITUDE*RELATIVE_AMPLITUDE*2.0*np.pi
        desired_pos=-np.sin(t*2*np.pi)*MAX_AMPLITUDE*RELATIVE_AMPLITUDE
        _head_pos.append(desired_pos)
        _head_vel.append(desired_speed)

    # single point over time
    head_pos = _head_pos[pt]
    head_vel = _head_vel[pt]

    head_pos = ((head_pos + 0.8) / 1.6)
    head_vel = ((head_vel + 0.8 * 2 * np.pi) / (1.6 * 2 * np.pi))

    if head_pos > 1.0:
        head_pos = 1.0
    elif head_pos < 0.0:
        head_pos = 0.0
    if head_vel > 1.0:
        head_vel = 1.0
    elif head_vel < 0.0:
        head_vel = 0.0

    min_rate = 0.0
    max_rate = 600.0
    sigma = 0.02
    MF_pos_activity = np.zeros((50))
    MF_vel_activity = np.zeros((50))

    for i in range(50):
        mean = float(i) / 50.0 + 0.01
        gaussian = np.exp(-((head_pos - mean) * (head_pos - mean))/(2.0 * sigma * sigma))
        MF_pos_activity[i] = min_rate + gaussian * (max_rate - min_rate)

    for i in range(50):
        mean = float(i) / 50.0 + 0.01
        gaussian = np.exp(-((head_vel - mean) * (head_vel - mean))/(2.0 * sigma * sigma))
        MF_vel_activity[i] = min_rate + gaussian * (max_rate - min_rate)

    #sa_mean_freq = np.arange(0,1000,10)
    sa_mean_freq = np.concatenate((MF_pos_activity, MF_vel_activity))
    out = [sa_mean_freq,head_pos,head_vel]
    return out

# Error Activity: error from eye and head encoders
def error_activity(pt):
    def compute_P_error(kp, head_position, eye_position):
        error = kp * (head_position + eye_position)
        return error
    def compute_D_error(kd, head_velocity, eye_velocity):
        error = kd * (head_velocity + eye_velocity)
        return error

    MAX_AMPLITUDE = 0.8
    MAX_AMPLITUDE_EYE = 0.35
    RELATIVE_AMPLITUDE_EYE = 1.0
    phaseShift  = 1.0*np.pi # simulated error between eye and head signals, error is zero if the waves are in opposite phase
    _eye_pos = []
    _eye_vel = []
    ea_rate = []
    i = np.arange(0,2,0.01)
    for t_eye in i:
        desired_speed = -np.cos(t_eye*2*np.pi+phaseShift) * MAX_AMPLITUDE_EYE * RELATIVE_AMPLITUDE_EYE * 2.0 * np.pi
        desired_pos = -np.sin(t_eye*2*np.pi+phaseShift) * MAX_AMPLITUDE_EYE * RELATIVE_AMPLITUDE_EYE
        _eye_pos.append(desired_pos)
        _eye_vel.append(desired_speed)

    # single point over time
    eye_pos = _eye_pos[pt]
    eye_vel = _eye_vel[pt]
    #print 'eye_pos ea',eye_pos

    head = sensorial_activity(pt)
    head_pos = head[1]
    head_vel = head[2]

    #print head_pos, eye_pos
    kp=15.0
    position_error = compute_P_error(kp, head_pos, eye_pos)
    kd=15.0
    velocity_error = compute_D_error(kd, head_vel, eye_vel)

    error=(position_error * 0.1 + (velocity_error/(2.0*np.pi)) * 0.9)/(MAX_AMPLITUDE*5)

    #print position_error, velocity_error, error

    min_rate = 1.0
    max_rate = 25.0
    err = np.linspace(-2.0, 2.0, 20)
#    err = [1]
    for j in range(len(err)):
        error_ = err[j]
        #print error_
        low_neuron_ID_threshold = abs(error_) * 100.0
        up_neuron_ID_threshold = low_neuron_ID_threshold - 100.0
        IO_agonist = np.zeros((100))
        IO_antagonist = np.zeros((100))

        rate = []
        for i in range (100):
            if(i < up_neuron_ID_threshold):
                rate.append(max_rate)
            elif(i<low_neuron_ID_threshold):
                aux_rate=max_rate - (max_rate-min_rate)*((i - up_neuron_ID_threshold)/(low_neuron_ID_threshold - up_neuron_ID_threshold))
                rate.append(aux_rate)
            else:
                rate.append(min_rate)

            if error_>=0.0:
                IO_agonist[0:100]=min_rate
                IO_antagonist=rate
            else:
                IO_antagonist[0:100]=min_rate
                IO_agonist=rate

            ea_rate = np.concatenate((IO_agonist,IO_antagonist))
        #print j
#         plt.plot(np.linspace(up_neuron_ID_threshold,low_neuron_ID_threshold,200) ,ea_rate)
#         plt.plot(ea_rate)
#     plt.show()

    low_neuron_ID_threshold = abs(error) * 100.0
    up_neuron_ID_threshold = low_neuron_ID_threshold - 100.0
    IO_agonist = np.zeros((100))
    IO_antagonist = np.zeros((100))

    rate = []
    for i in range (100):
        if(i < up_neuron_ID_threshold):
            rate.append(max_rate)
        elif(i<low_neuron_ID_threshold):
            aux_rate=max_rate - (max_rate-min_rate)*((i - up_neuron_ID_threshold)/(low_neuron_ID_threshold - up_neuron_ID_threshold))
            rate.append(aux_rate)
        else:
            rate.append(min_rate)

        if error>=0.0:
            IO_agonist[0:100]=min_rate
            IO_antagonist=rate
        else:
            IO_antagonist[0:100]=min_rate
            IO_agonist=rate

        ea_rate = np.concatenate((IO_agonist,IO_antagonist))

#     plt.plot(ea_rate)
#     plt.show()

    return ea_rate

####


for j in range (200):
    x = error_activity(j)
    plt.plot(x)

plt.show()

SA_population = sim.Population(num_MF_neurons, # number of sources
                        sim.SpikeSourcePoisson, # source type
                        #{'rate': sa_mean_freq}, # source spike times
                        {'rate': sensorial_activity(10)[0]}, # source spike times
                        label="sa_population" # identifier
                        )
# plt.plot(sensorial_activity())
# plt.show()
# Create MF population
MF_population = sim.Population(num_MF_neurons, sim.IF_curr_exp(),label='MFLayer')

# Create GOC population
GOC_population = sim.Population(num_GOC_neurons, sim.IF_cond_exp() ,label='GOCLayer')

# Create MF-GO connections
mf_go_connections = sim.Projection(MF_population,
                                   GOC_population,
                                   sim.OneToOneConnector(),
                                   sim.StaticSynapse(delay=1.0, weight=mf_go_weights))

# Create GrC population
GC_population = sim.Population(num_GC_neurons,sim.IF_curr_exp(),label='GCLayer')

# create PC population
PC_population = sim.Population(num_PC_neurons, # number of neurons
                       sim.extra_models.IFCondExpCerebellum(**neuron_params),  # Neuron model
                       label="Purkinje Cell" # identifier
                       )

# create VN population
VN_population = sim.Population(num_VN_neurons, # number of neurons
                       sim.extra_models.IFCondExpCerebellum(**neuron_params),  # Neuron model
                       label="Vestibular Nuclei" # identifier
                       )

# Create IO population
IO_population = sim.Population(num_IO_neurons,sim.IF_curr_exp(),label='IOLayer')

# Create connections

# Create MF-GC and GO-GC connections
float_num_MF_neurons = float (num_MF_neurons)

list_GOC_GC = []
list_MF_GC = []
list_GOC_GC_2 = []
# projections to subpopulations https://github.com/SpiNNakerManchester/sPyNNaker8/issues/168)
for i in range (num_MF_neurons):
        GC_medium_index = int(round((i / float_num_MF_neurons ) * num_GC_neurons))
        GC_lower_index = GC_medium_index - 40
        GC_upper_index = GC_medium_index + 60

        if(GC_lower_index < 0):
                GC_lower_index = 0

        elif(GC_upper_index > num_GC_neurons):
                GC_upper_index = num_GC_neurons

        for j in range (GC_medium_index - GC_lower_index):
            list_GOC_GC.append((i, GC_lower_index + j))

        for j in range(GC_medium_index + 20 - GC_medium_index):
            list_MF_GC.append((i, GC_medium_index + j))


        for j in range(GC_upper_index - GC_medium_index - 20):
            list_GOC_GC_2.append((i, GC_medium_index + 20 + j))

GO_GC_con1 = sim.Projection(GOC_population,
              GC_population,
              sim.FromListConnector(list_GOC_GC, weight_distr_GO, delay_distr))

MF_GC_con2 = sim.Projection(MF_population,
              GC_population,
              sim.FromListConnector(list_MF_GC, weight_distr_MF, delay_distr))

GO_GC_con3 = sim.Projection(GOC_population,
              GC_population,
              sim.FromListConnector(list_GOC_GC_2, weight_distr_GO, delay_distr))


# Create PC-VN connections
pc_vn_connections = sim.Projection(PC_population,
                               VN_population,
                               sim.OneToOneConnector(),
                               #receptor_type='GABA',
                               synapse_type = sim.StaticSynapse(delay=1.0, weight=pc_vn_weights))

# Create MF-VN learning rule - cos
mfvn_plas = sim.STDPMechanism(
    timing_dependence=sim.extra_models.TimingDependenceMFVN(beta=beta_c,
                                                          sigma=sigma_c),
    weight_dependence=sim.extra_models.WeightDependenceMFVN(w_min=min_weight_c,
                                                          w_max=max_weight_c,
                                                          pot_alpha=pot_alpha_c),
    weight=initial_weight_c, delay=plastic_delay_c)

# Create MF to VN connections
mf_vn_connections = sim.Projection(
    MF_population, VN_population, sim.AllToAllConnector(),
    synapse_type=mfvn_plas, receptor_type="excitatory")

# Create projection from PC to VN -- replaces "TEACHING SIGNAL"
pc_vn_connections = sim.Projection(
    PC_population, VN_population, sim.OneToOneConnector(),
    sim.StaticSynapse(weight=0.0, delay=1), receptor_type="excitatory")

# create PF-PC learning rule - sin
pfpc_plas = sim.STDPMechanism(
    timing_dependence=sim.extra_models.TimingDependencePFPC(t_peak=t_peak_s),
    weight_dependence=sim.extra_models.WeightDependencePFPC(w_min=min_weight_s,
                                                          w_max=max_weight_s,
                                                          pot_alpha=pot_alpha_s),
    weight=initial_weight_s, delay=plastic_delay_s)

# Create PF-PC connections
pf_pc_connections = sim.Projection(
    GC_population, PC_population, sim.AllToAllConnector(),
    synapse_type=pfpc_plas, receptor_type="excitatory")

# Create IO-PC connections. This synapse with "receptor_type=COMPLEX_SPIKE" propagates the learning signals that drive the plasticity mechanisms in GC-PC synapses
io_pc_connections = sim.Projection(IO_population,
                               PC_population,
                               sim.OneToOneConnector(),
                               #receptor_type='COMPLEX_SPIKE',
                               synapse_type = sim.StaticSynapse(delay=1.0, weight=io_pc_weights))



lif_pop = sim.Population(1024, sim.IF_curr_exp(), label='pop_lif')

out_pop = sim.Population(128, sim.IF_curr_exp(), label='pop_out')



# sim.Projection(
#     lif_pop, out_pop, sim.OneToOneConnector(),
#     synapse_type=sim.StaticSynapse(weight=0.1))
#
#
# # live output of the input vertex (retina_pop) to the first pynn population (lif_pop)
# sim.external_devices.activate_live_output_to(out_pop,retina_pop)
#
#
# #recordings and simulations
# lif_pop.record(["spikes"])
#
# out_pop.record(["spikes"])
#
#
#
# sim.run(10)
#
# sim.end()

