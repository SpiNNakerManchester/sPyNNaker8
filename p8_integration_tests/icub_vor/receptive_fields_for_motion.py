import socket
import spynnaker8 as sim
import numpy as np
#import logging
import matplotlib.pyplot as plt

from pacman.model.constraints.key_allocator_constraints import FixedKeyAndMaskConstraint
from pacman.model.graphs.application import ApplicationSpiNNakerLinkVertex
from pacman.model.routing_info import BaseKeyAndMask
from spinn_front_end_common.abstract_models.abstract_provides_n_keys_for_partition import AbstractProvidesNKeysForPartition
from spinn_front_end_common.abstract_models.abstract_provides_outgoing_partition_constraints import AbstractProvidesOutgoingPartitionConstraints
from spinn_utilities.overrides import overrides
from spinn_front_end_common.abstract_models.abstract_provides_incoming_partition_constraints import AbstractProvidesIncomingPartitionConstraints
from pacman.executor.injection_decorator import inject_items
from pacman.operations.routing_info_allocator_algorithms.malloc_based_routing_allocator.utils import get_possible_masks
from spinn_front_end_common.utility_models.command_sender_machine_vertex import CommandSenderMachineVertex

from spinn_front_end_common.abstract_models \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utility_models.multi_cast_command \
    import MultiCastCommand


from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import RandomDistribution, NumpyRNG

from spynnaker.pyNN.models.neuron.plasticity.stdp.common import plasticity_helpers

NUM_NEUR_IN = 1024 #1024 # 2x240x304 mask -> 0xFFFE0000
MASK_IN = 0xFFFFFC00 #0xFFFFFC00
NUM_NEUR_OUT = 1024
MASK_OUT =0xFFFFFC00

class ICUBInputVertex(
        ApplicationSpiNNakerLinkVertex,
        AbstractProvidesOutgoingPartitionConstraints,
        AbstractProvidesIncomingPartitionConstraints,
        AbstractSendMeMulticastCommandsVertex):

    def __init__(self, spinnaker_link_id, board_address=None,
                 constraints=None, label=None):

        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_atoms=NUM_NEUR_IN, spinnaker_link_id=spinnaker_link_id,
            board_address=board_address, label=label)

        AbstractProvidesNKeysForPartition.__init__(self)
        AbstractProvidesOutgoingPartitionConstraints.__init__(self)
        AbstractSendMeMulticastCommandsVertex.__init__(self)

    @overrides(AbstractProvidesOutgoingPartitionConstraints.
               get_outgoing_partition_constraints)
    def get_outgoing_partition_constraints(self, partition):
        return [FixedKeyAndMaskConstraint(
            keys_and_masks=[BaseKeyAndMask(
                base_key=0, #upper part of the key,
                mask=MASK_IN)])]
                #keys, i.e. neuron addresses of the input population that sits in the ICUB vertex,

    @inject_items({"graph_mapper": "MemoryGraphMapper"})
    @overrides(AbstractProvidesIncomingPartitionConstraints.
               get_incoming_partition_constraints,
               additional_arguments=["graph_mapper"])
    def get_incoming_partition_constraints(self, partition, graph_mapper):
        if isinstance(partition.pre_vertex, CommandSenderMachineVertex):
            return []
        index = graph_mapper.get_machine_vertex_index(partition.pre_vertex)
        vertex_slice = graph_mapper.get_slice(partition.pre_vertex)
        mask = get_possible_masks(vertex_slice.n_atoms)[0]
        key = (0x1000 + index) << 16
        return [FixedKeyAndMaskConstraint(
            keys_and_masks=[BaseKeyAndMask(key, mask)])]

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):
        return [MultiCastCommand(
            key=0x80000000, payload=0, repeat=5, delay_between_repeats=100)]

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        return [MultiCastCommand(
            key=0x40000000, payload=0, repeat=5, delay_between_repeats=100)]

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []


def map_neurons_to_field(length, x_segments, y_segments, scale_down, layers, x_size=304, y_size=240, central_x=38,
                         central_y=30):
    # base-filter = width x (dimension / segments)
    # Y*8 E*2 X*9 P*1
    # x_segments /= 2
    # y_segments /= 2
    field_size_x = []
    field_size_y = []
    # define the field size for each layer
    for i in range(layers):
        field_size_length_x = length * (scale_down ** layers)
        field_size_width_x = (x_size / x_segments) * (scale_down ** layers)
        field_size_x.append([field_size_length_x, field_size_width_x])
        field_size_length_y = length * (scale_down ** layers)
        field_size_width_y = (y_size / y_segments) * (scale_down ** layers)
        field_size_y.append([field_size_length_y, field_size_width_y])

    # map the field size to real pixels
    pixel_mapping = [[[[-1, -1] for x in range(y_size)] for y in range(x_size)] for i in range(layers + 1)]
    field_size = [[[0 for i in range(y_segments)] for j in range(x_segments)] for k in range(layers)]
    for x in range(central_x / 2):
        for y in range(central_y / 2):
            pixel_mapping[layers][(x_size / 2) + x][(y_size / 2) - y] = [0, 0]
            pixel_mapping[layers][(x_size / 2) - x][(y_size / 2) + y] = [0, 0]
            pixel_mapping[layers][(x_size / 2) + x][(y_size / 2) + y] = [0, 0]
            pixel_mapping[layers][(x_size / 2) - x][(y_size / 2) - y] = [0, 0]
    for layer in range(layers):
        x_border = int(x_size - (x_size * (scale_down ** layer)))  # / 2
        y_border = int(y_size - (y_size * (scale_down ** layer)))  # / 2
        if x_border < x_size / 2 or y_border < y_size / 2:
            for x in range(0, (x_size / 2) - x_border):
                for y in range(0, (y_size / 2) - y_border):
                    if x < length * (scale_down ** layer) or y < length * (scale_down ** layer):
                        x_segment = int(x / ((x_size - (x_border * 2)) / x_segments))
                        y_segment = int(y / ((y_size - (y_border * 2)) / y_segments))
                        pixel_mapping[layer][x + x_border][y + y_border] = \
                            [x_segment, y_segment]
                        field_size[layer][x_segment][y_segment] += 1
                        pixel_mapping[layer][((x_size - 1) - x_border) - x][((y_size - 1) - y_border) - y] = \
                            [(x_segments - 1) - x_segment, (y_segments - 1) - y_segment]
                        field_size[layer][(x_segments - 1) - x_segment][(y_segments - 1) - y_segment] += 1
                        pixel_mapping[layer][x + x_border][((y_size - 1) - y_border) - y] = \
                            [x_segment, (y_segments - 1) - y_segment]
                        field_size[layer][x_segment][(y_segments - 1) - y_segment] += 1
                        pixel_mapping[layer][((x_size - 1) - x_border) - x][y + y_border] = \
                            [(x_segments - 1) - x_segment, y_segment]
                        field_size[layer][(x_segments - 1) - x_segment][y_segment] += 1
                        # print x, x_segment, x_segments, y, y_segment, y_segments
            # print x, y
        print "finished layer", layer, "with border", x_border, y_border

    print "done mapping"
    return pixel_mapping, field_size


def map_to_from_list(mapping, width, length, scale_down, pixel_weight=0.03, x_size=304, y_size=240, motor_weight=0.04):
    mapping, field_size = mapping
    layers = len(mapping)
    print "layer", layers, "width", width, "length", length
    from_list_connections = [[] for i in range(layers)]
    motor_conn = []
    for layer in range(layers):
        motor_control_e = []
        motor_control_i = []
        for x in range(x_size):
            for y in range(y_size):
                if mapping[layer][x][y][0] != -1:
                    if layer < layers - 1:
                        weight = pixel_weight / field_size[layer][mapping[layer][x][y][0]][mapping[layer][x][y][1]]
                    else:
                        weight = pixel_weight
                    from_list_connections[layer].append(
                        [x + (304 * y),
                         (mapping[layer][x][y][0] + mapping[layer][x][y][1] * width),
                         1,
                         weight])
        for connection in from_list_connections[layer]:
            if connection[1] < width / 2:
                motor_control_e.append([connection[1], 0, 1, 0.1])
                motor_control_i.append([connection[1], 1, 1, 0.1])
            if connection[1] > width / 2:
                motor_control_e.append([connection[1], 1, 1, 0.1])
                motor_control_i.append([connection[1], 0, 1, 0.1])
            if connection[1] < length / 2:
                motor_control_e.append([connection[1], 2, 1, 0.1])
                motor_control_i.append([connection[1], 3, 1, 0.1])
            if connection[1] > length / 2:
                motor_control_e.append([connection[1], 3, 1, 0.1])
                motor_control_i.append([connection[1], 2, 1, 0.1])
        motor_conn.append([motor_control_e, motor_control_i])
    print "created connections"
    return from_list_connections, motor_conn


def connect_it_up(visual_input, motor_output, connections, width, length):
    visual_connections, motor_conn = connections
    layers = len(motor_conn)
    hidden_pops = []
    for layer in range(layers):
        motor_conn_e, motor_conn_i = motor_conn[layer]
        hidden_pop = sim.Population(width * 2 + length * 2 - 2, sim.IF_curr_exp(), label="hidden_pop_{}".format(layer))
        hidden_pops.append(hidden_pop)
        sim.Projection(visual_input, hidden_pop, sim.FromListConnector(visual_connections[layer]))
        sim.Projection(hidden_pop, motor_output, sim.FromListConnector(motor_conn_e))
        sim.Projection(hidden_pop, motor_output, sim.FromListConnector(motor_conn_i), receptor_type="inhibitory")
    print "finished connecting"


sim.setup(timestep=1.0)
# sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 255)

mapping_1 = map_neurons_to_field(64, 19, 15, 0.9, 5)
mapping_2 = map_neurons_to_field(20, 19, 15, 0.9, 5)
mapping_3 = map_neurons_to_field(50, 19, 15, 0.9, 5)
mapping_4 = map_neurons_to_field(128, 2, 2, 0.9, 5)
mapping_5 = map_neurons_to_field(128, 2, 2, 0.9, 7)
print "created mapping"
connections_1 = map_to_from_list(mapping_1, 19, 15, 0.9)
connections_2 = map_to_from_list(mapping_2, 19, 15, 0.9)
connections_3 = map_to_from_list(mapping_3, 19, 15, 0.9)
connections_4 = map_to_from_list(mapping_4, 2, 2, 0.9)
connections_5 = map_to_from_list(mapping_5, 2, 2, 0.9)
print "created all connections"


sim.setup(timestep=1.0)
# sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 32)

# set up populations,
vis_pop = sim.Population(None, ICUBInputVertex(spinnaker_link_id=0), label='pop_in')

#neural population    ,
neuron_pop = sim.Population(NUM_NEUR_OUT, sim.IF_curr_exp(), label='neuron_pop')

pop_out = sim.Population(4, sim.IF_curr_exp(), label="motor_control")

connect_it_up(vis_pop, pop_out, connections_1, 19, 15)
connect_it_up(vis_pop, pop_out, connections_2, 19, 15)
connect_it_up(vis_pop, pop_out, connections_3, 19, 15)
connect_it_up(vis_pop, pop_out, connections_4, 2, 2)
connect_it_up(vis_pop, pop_out, connections_5, 2, 2)

# sim.Projection(pop, neuron_pop, sim.OneToOneConnector(), sim.StaticSynapse(weight=20.0))

#pop_out = sim.Population(None, ICUBOutputVertex(spinnaker_link_id=0), label='pop_out')

sim.external_devices.activate_live_output_to(pop_out, vis_pop)


#recordings and simulations,
#neuron_pop.record("spikes")

simtime = 30000 #ms,
#sim.run(simtime)

# continuous run until key press
# remember: do NOT record when running in this mode
sim.external_devices.run_forever()
raw_input('Press enter to stop')

# #exc_spikes = neuron_pop.get_data("spikes")
#
# Figure(
#     # raster plot of the neuron_pop
#     Panel(exc_spikes.segments[0].spiketrains, xlabel="Time/ms", xticks=True,
#           yticks=True, markersize=0.2, xlim=(0, simtime)),
#     title="neuron_pop: spikes"
# )
# plt.show()

sim.end()

print("finished")
