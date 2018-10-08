import socket
import spynnaker8 as sim
import numpy as np
#import logging
import matplotlib.pyplot as plt

from spynnaker8.utilities import DataHolder
from pacman.model.constraints.key_allocator_constraints import FixedKeyAndMaskConstraint
from pacman.model.graphs.application import ApplicationSpiNNakerLinkVertex
from pacman.model.routing_info import BaseKeyAndMask
from spinn_front_end_common.abstract_models.abstract_provides_n_keys_for_partition import AbstractProvidesNKeysForPartition
from spinn_front_end_common.abstract_models.abstract_provides_outgoing_partition_constraints import AbstractProvidesOutgoingPartitionConstraints
from spinn_utilities.overrides import overrides
from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import RandomDistribution, NumpyRNG

RETINA_X_SIZE = 304
RETINA_Y_SIZE = 240
RETINA_BASE_KEY = 0x00000000
RETINA_MASK = 0xFF000000
RETINA_Y_BIT_SHIFT = 9

class ICUBInputVertex(
        ApplicationSpiNNakerLinkVertex,
        # AbstractProvidesNKeysForPartition,
         AbstractProvidesOutgoingPartitionConstraints):

    def __init__(self, n_neurons, spinnaker_link_id, board_address=None,
                 constraints=None, label=None):

        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_neurons, spinnaker_link_id=spinnaker_link_id,
            board_address=board_address, label=label, constraints=constraints)
        #AbstractProvidesNKeysForPartition.__init__(self)
        AbstractProvidesOutgoingPartitionConstraints.__init__(self)

#    @overrides(AbstractProvidesNKeysForPartition.get_n_keys_for_partition)
#    def get_n_keys_for_partition(self, partition, graph_mapper):
#        return 1048576

    @overrides(AbstractProvidesOutgoingPartitionConstraints.
               get_outgoing_partition_constraints)
    def get_outgoing_partition_constraints(self, partition):
        return [FixedKeyAndMaskConstraint(
            keys_and_masks=[BaseKeyAndMask(
                base_key=0, #upper part of the key
                mask=0xFFFFFC00)])]
                #keys, i.e. neuron addresses of the input population that sits in the ICUB vertex
                # this mask removes all spikes that have a "1" in the MSB and lets the spikes go only if the MSB are at "0"
                # it must have enough keys to host the input addressing space and the output (with the same keys)
class ICUBInputVertexDataHolder(DataHolder):

    def __init__(self, spinnaker_link_id, board_address=None,
                 constraints=None, label=None):
        DataHolder.__init__(
            self, {"spinnaker_link_id": spinnaker_link_id,"board_address": board_address, "label": label})

    @staticmethod
    def build_model():
        return ICUBInputVertex
#logger = logging.getLogger(__name__)

# Synapsis parameters
gc_pc_weights = 0.005
mf_vn_weights = 0.001
pc_vn_weights = 0.00002
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

GO_PARAMS = {'cm': 0.002,
             'v_rest': -70.0,
             'tau_m': 100.0,
             'e_rev_E': 0.0,
             'e_rev_I': -75.0,
             'v_reset': -70.0,
             'v_thresh': -40.0,
             'tau_refrac': 1.0,
             'tau_syn_E': 0.5,
             'tau_syn_I': 2.0}


sim.setup(timestep=1.)
#sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 255)

# set up populations
num_pxl = 304 * 240;
retina_pop = sim.Population(1024, ICUBInputVertexDataHolder(spinnaker_link_id=0), label='pop_retina')



# Create GOC population
# Create MF population

#MF_population = sim.Population(num_MF_neurons,parrot_neuron,{},label='MFLayer')
MF_population = sim.Population(num_MF_neurons, sim.IF_curr_exp(),label='MFLayer')

# Create GOC population
#GOC_population = sim.Population(num_GOC_neurons,spynnaker.pyNN.models.neuron.builds.if_cond_alpha.IFCondAlpha(),label='GOCLayer')
GOC_population = sim.Population(num_GOC_neurons, sim.IF_cond_exp() ,label='GOCLayer')

# Create MF-GO connections
mf_go_connections = sim.Projection(MF_population,
                                   GOC_population,
                                   sim.OneToOneConnector(),
                                   sim.StaticSynapse(delay=1.0, weight=mf_go_weights))

# Create GrC population
#GC_population = sim.Population(num_GC_neurons,sim.IF_cond_alpha(**GR_PARAMS),label='GCLayer')
GC_population = sim.Population(num_GC_neurons,sim.IF_curr_exp(),label='GCLayer')

# Random distribution for synapses delays and weights
delay_distr = RandomDistribution('uniform', (1.0, 10.0), rng=NumpyRNG(seed=85524))
weight_distr_MF = RandomDistribution('uniform', (mf_gc_weights*0.8, mf_gc_weights*1.2), rng=NumpyRNG(seed=85524))
weight_distr_GO = RandomDistribution('uniform', (go_gc_weights*0.8, go_gc_weights*1.2), rng=NumpyRNG(seed=24568))


# Create MF-GC and GO-GC connections
float_num_MF_neurons = float (num_MF_neurons)


list_GOC_GC = []
list_MF_GC = []
list_GOC_GC_2 = []
for i in range (num_MF_neurons):
        GC_medium_index = int(round((i / float_num_MF_neurons ) * num_GC_neurons))
        GC_lower_index = GC_medium_index - 40
        GC_upper_index = GC_medium_index + 60

        #print GC_lower_index, GC_medium_index, GC_upper_index

        if(GC_lower_index < 0):
                GC_lower_index = 0

        elif(GC_upper_index > num_GC_neurons):
                GC_upper_index = num_GC_neurons

        for j in range (GC_medium_index - GC_lower_index):
            list_GOC_GC.append((i, GC_lower_index + j))

        for j in range(GC_medium_index + 20 - GC_medium_index):
            list_MF_GC.append((i, GC_medium_index + j))

        for j in range(GC_upper_index - GC_medium_index + 20):
            list_GOC_GC_2.append((i, GC_medium_index + 20 + j))

GO_GC_con1 = sim.Projection(GOC_population,
              GC_population,
              sim.FromListConnector(list_GOC_GC, weight_distr_GO, delay_distr))
              #sim.StaticSynapse(delay=delay_distr, weight=weight_distr_GO))


MF_GC_con2 = sim.Projection(MF_population,
              GC_population,
              sim.FromListConnector(list_MF_GC, weight_distr_MF, delay_distr))
              #sim.StaticSynapse(delay=delay_distr, weight=weight_distr_MF))

GO_GC_con3 = sim.Projection(GOC_population,
              GC_population,
              sim.FromListConnector(list_GOC_GC_2, weight_distr_GO, delay_distr))
              #sim.StaticSynapse(delay=delay_distr, weight=weight_distr_GO))


#PC_population = sim.Population(num_PC_neurons,pc_neuron(**PC_PARAMS),label='PCLayer')
PC_population = sim.Population(num_PC_neurons,sim.IF_curr_exp(),label='PCLayer')


#VN_population = sim.Population(num_VN_neurons,vn_neuron(**VN_PARAMS),label='VNLayer')
VN_population = sim.Population(num_VN_neurons,sim.IF_curr_exp(),label='VNLayer')


# Create IO population
#IO_population = sim.Population(num_IO_neurons,parrot_neuron,{},label='IOLayer')
IO_population = sim.Population(num_IO_neurons,sim.IF_curr_exp(),label='IOLayer')



# # Create MF-VN learning rule (THIS MODEL HAS BEEN DEFINED IN THE CEREBELLUMMODULE PACKAGE: https://github.com/jgarridoalcazar/SpikingCerebellum/)
# stdp_cos = sim.native_synapse_type('stdp_cos_synapse')(**{'weight':mf_vn_weights,
#                                                       'delay':1.0,
#                                                       'exponent': 2.0,
#                                                       'tau_cos': 5.0,
#                                                       'A_plus': 0.0000009,
#                                                       'A_minus': 0.00001,
#                                                       'Wmin': 0.0005,
#                                                       'Wmax': 0.007})

# Create PC-VN connections
pc_vn_connections = sim.Projection(PC_population,
                               VN_population,
                               sim.OneToOneConnector(),
                               #receptor_type='GABA',
                               synapse_type = sim.StaticSynapse(delay=1.0, weight=pc_vn_weights))


# This second synapse with "receptor_type=TEACHING_SIGNAL" propagates the learning signals that drive the plasticity mechanisms in MF-VN synapses
pc_vn_connections = sim.Projection(PC_population,
                               VN_population,
                               sim.OneToOneConnector(),
                               #receptor_type='TEACHING_SIGNAL',
                               synapse_type = sim.StaticSynapse(delay=1.0, weight=0.0))


timing_rule = sim.SpikePairRule(tau_plus=20.0, tau_minus=20.0,
                                A_plus=0.5, A_minus=0.5)
weight_rule = sim.AdditiveWeightDependence(w_max=5.0, w_min=0.0)

stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=0.0, delay=5.0)

mf_vn_connections = sim.Projection(MF_population, VN_population, sim.AllToAllConnector(),
                                 synapse_type=stdp_model)


# # Create MF-VN learning rule (THIS MODEL HAS BEEN DEFINED IN THE CEREBELLUMMODULE PACKAGE: https://github.com/jgarridoalcazar/SpikingCerebellum/)
# stdp_syn = sim.native_synapse_type('stdp_sin_synapse')(**{'weight':gc_pc_weights,
#                                                       'delay':1.0,
#                                                       'exponent': 10,
#                                                       'peak': 100.0,
#                                                       'A_plus': 0.000014,
#                                                       'A_minus': 0.00008,
#                                                       'Wmin': 0.000,
#                                                       'Wmax': 0.010})

# Create GC-PC connections
gc_pc_connections = sim.Projection(GC_population, PC_population, sim.AllToAllConnector(),
                                 synapse_type=stdp_model)
# Create IO-PC connections. This synapse with "receptor_type=COMPLEX_SPIKE" propagates the learning signals that drive the plasticity mechanisms in GC-PC synapses
io_pc_connections = sim.Projection(IO_population,
                               PC_population,
                               sim.OneToOneConnector(),
                               #receptor_type='COMPLEX_SPIKE',
                               synapse_type = sim.StaticSynapse(delay=1.0, weight=io_pc_weights))



lif_pop = sim.Population(1024, sim.IF_curr_exp(), label='pop_lif')

out_pop = sim.Population(128, sim.IF_curr_exp(), label='pop_out')



sim.Projection(
    lif_pop, out_pop, sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=0.1))


# live output of the input vertex (retina_pop) to the first pynn population (lif_pop)
sim.external_devices.activate_live_output_to(out_pop,retina_pop)


#recordings and simulations
lif_pop.record(["spikes"])

out_pop.record(["spikes"])



sim.run(10)

sim.end()

