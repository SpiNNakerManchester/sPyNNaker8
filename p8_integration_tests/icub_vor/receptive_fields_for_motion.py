#!usr/bin/python

import socket
import spynnaker8 as sim
import numpy as np
#import logging
import matplotlib.pyplot as plt
from decode_events import*
from functions import*
import yarp

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

# yarp.Network.init()

NUM_NEUR_IN = 1024 #1024 # 2x240x304 mask -> 0xFFFE0000
MASK_IN = 0xFFFFFC00 #0xFFFFFC00
NUM_NEUR_OUT = 1024
MASK_OUT =0xFFFFFFFC

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

def convert_data_mapping(x, y, down_sample_x, down_sample_y):
    if simulate:
        x /= (304 / down_sample_x)
        y /= (240 / down_sample_y)
        address = (y * 304) + x
    else:
        address = (int(y) << 12) + (int(x) << 1) + 1
    return int(address)

def convert_data(data):
    converted_data = [[] for i in range(304*240)]
    for item in data:
        converted_data[convert_data_mapping(item[2], item[3], width, length)].append(item[0]*1000)
    return converted_data

def convert_pixel_mapping(pixel, down_sample_x, down_sample_y):
    x = pixel % 304
    y = (pixel - x) / 304
    if simulate:
        x /= (304 / down_sample_x)
        y /= (240 / down_sample_y)
        address = (y * down_sample_x) + x
    else:
        address = (y << 12) + (x << 1) + 1
    return address

def map_neurons_to_field(length, x_segments, y_segments, scale_down, layers, x_size=304, y_size=240, central_x=304,
                         central_y=240):
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
    field_size = [[[0 for i in range(y_segments)] for j in range(x_segments)] for k in range(layers+1)]
    x_border = int(x_size - central_x)  # / 2
    y_border = int(y_size - central_y)  # / 2
    for x in range(central_x / 2):
        for y in range(central_y / 2):
            x_segment = int(x / ((x_size - (x_border)) / x_segments))
            y_segment = int(y / ((y_size - (y_border)) / y_segments))
            pixel_mapping[layers][(x_size - (x_border / 2)) - x -1][y + y_border] = [(x_segments - 1) - x_segment, y_segment]
            pixel_mapping[layers][x + x_border][(y_size - (y_border / 2)) - y - 1] = [x_segment, (y_segments - 1) - y_segment]
            pixel_mapping[layers][(x_size - (x_border / 2)) - x - 1][(y_size - (y_border / 2)) - y - 1] = [(x_segments - 1) - x_segment, (y_segments - 1) - y_segment]
            pixel_mapping[layers][x + x_border][y + y_border] = [x_segment, y_segment]
    # for layer in range(layers):
    #     x_border = int(x_size - (x_size * (scale_down ** layer)))  # / 2
    #     y_border = int(y_size - (y_size * (scale_down ** layer)))  # / 2
    #     if x_border < x_size / 2 or y_border < y_size / 2:
    #         for x in range(0, (x_size / 2) - x_border):
    #             for y in range(0, (y_size / 2) - y_border):
    #                 if x < length * (scale_down ** layer) or y < length * (scale_down ** layer):
    #                     x_segment = int(x / ((x_size - (x_border * 2)) / x_segments))
    #                     y_segment = int(y / ((y_size - (y_border * 2)) / y_segments))
    #                     pixel_mapping[layer][x + x_border][y + y_border] = \
    #                         [x_segment, y_segment]
    #                     field_size[layer][x_segment][y_segment] += 1
    #                     pixel_mapping[layer][((x_size - 1) - x_border) - x][((y_size - 1) - y_border) - y] = \
    #                         [(x_segments - 1) - x_segment, (y_segments - 1) - y_segment]
    #                     field_size[layer][(x_segments - 1) - x_segment][(y_segments - 1) - y_segment] += 1
    #                     pixel_mapping[layer][x + x_border][((y_size - 1) - y_border) - y] = \
    #                         [x_segment, (y_segments - 1) - y_segment]
    #                     field_size[layer][x_segment][(y_segments - 1) - y_segment] += 1
    #                     pixel_mapping[layer][((x_size - 1) - x_border) - x][y + y_border] = \
    #                         [(x_segments - 1) - x_segment, y_segment]
    #                     field_size[layer][(x_segments - 1) - x_segment][y_segment] += 1
    #                     # print x, x_segment, x_segments, y, y_segment, y_segments
    #         # print x, y
    #     print "finished layer", layer, "with border", x_border, y_border

    print "done mapping"
    return pixel_mapping, field_size

def convert_xy_field_to_id(field_x, field_y, width, length):
    # receptive_fields = width * 2 + length * 2 - 2
    id = (field_y * width) + field_x
    return id

def map_to_from_list(mapping, width, length, scale_down, pixel_weight=5, x_size=304, y_size=240, motor_weight=1.5):
    # motor_weight *= width * length
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
                        weight = pixel_weight / float(field_size[layer][mapping[layer][x][y][0]][mapping[layer][x][y][1]])
                    else:
                        weight = pixel_weight #/ 16.
                    connection = [convert_pixel_mapping(x + (304 * y), width, length),
                                  convert_xy_field_to_id(mapping[layer][x][y][0], mapping[layer][x][y][1], width, length),
                                  weight,
                                  1]
                    if connection not in from_list_connections:
                        from_list_connections[layer].append(connection)
                    print x, y, x + (304 * y), convert_pixel_mapping(x + (304 * y), width, length), convert_xy_field_to_id(mapping[layer][x][y][0], mapping[layer][x][y][1], width, length)
                    if convert_pixel_mapping(x + (304 * y), width, length) >= 304*240 or convert_xy_field_to_id(mapping[layer][x][y][0], mapping[layer][x][y][1], width, length) >= width*length:
                        print "fucked"
        for connection in from_list_connections[layer]:
            if connection[1] % width < width / 2:
                if [connection[1], 0, motor_weight, 1] not in motor_control_e:
                    motor_control_e.append([connection[1], 0, motor_weight, 1])
                    motor_control_i.append([connection[1], 1, motor_weight, 1])
            if connection[1] % width > width / 2:
                if [connection[1], 1, motor_weight, 1] not in motor_control_e:
                    motor_control_e.append([connection[1], 1, motor_weight, 1])
                    motor_control_i.append([connection[1], 0, motor_weight, 1])
            if connection[1] / width < length / 2:
                if [connection[1], 2, motor_weight, 1] not in motor_control_e:
                    motor_control_e.append([connection[1], 2, motor_weight, 1])
                    motor_control_i.append([connection[1], 3, motor_weight, 1])
            if connection[1] / width > length / 2:
                if [connection[1], 3, motor_weight, 1] not in motor_control_e:
                    motor_control_e.append([connection[1], 3, motor_weight, 1])
                    motor_control_i.append([connection[1], 2, motor_weight, 1])
        motor_conn.append([motor_control_e, motor_control_i])
    print "created connections"
    return from_list_connections, motor_conn

def split_the_from_list(input, output, from_list, receptor_type="excitatory", max_conn=255):
    # from_list_segments = [from_list[x:x + max_conn] for x in xrange(0, len(from_list), max_conn)]
    # file_name = "connections.txt"
    # with open(file_name, 'w') as f:
    #     for segment in from_list_segments:
    #         connections_file = open(file_name, "w")
    #         for connection in segment:
    #             for item in connection:
    #                 f.write("%s " % item)
    #             f.write("\n")
    #         connections_file.close()
    #         sim.Projection(input, output, sim.FromFileConnector(file_name), receptor_type=receptor_type)

    from_list_segments = [from_list[x:x + max_conn] for x in xrange(0, len(from_list), max_conn)]
    for connection in from_list_segments:
        sim.Projection(input, output, sim.FromListConnector(connection), receptor_type=receptor_type)

def segment_hidden_pop(from_list, width, length, pre):
    hidden_pops = []
    list_of_lists = [[] for i in range(width*length)]
    for connection in from_list:
        if pre:
            list_of_lists[connection[0]].append([0, connection[1], connection[2], connection[3]])
        else:
            list_of_lists[connection[1]].append([connection[0], 0, connection[2], connection[3]])
    return list_of_lists

def connect_it_up(visual_input, motor_output, connections, width, length):
    visual_connections, motor_conn = connections
    layers = len(motor_conn)
    all_pops = []
    hidden_pops = []
    for layer in range(layers):
        motor_conn_e, motor_conn_i = motor_conn[layer]
        # hidden_pop = sim.Population(width * length, sim.IF_curr_exp(), label="hidden_pop_{}".format(layer))
        # hidden_pops.append(hidden_pop)
        for i in range(width*length):
            hidden_pop = sim.Population(1, sim.IF_curr_exp(tau_refrac=3), label="hidden_pop_{}_{}".format(layer, i))
            if simulate:
                hidden_pop.record(["spikes", "v"])
            hidden_pops.append(hidden_pop)
        list_of_lists = segment_hidden_pop(visual_connections[layer], width, length, False)
        for i in range(len(list_of_lists)):
            split_the_from_list(visual_input, hidden_pops[i], list_of_lists[i])
        list_of_lists = segment_hidden_pop(motor_conn_e, width, length, True)
        for i in range(len(list_of_lists)):
            split_the_from_list(hidden_pops[i], motor_output, list_of_lists[i])
        list_of_lists = segment_hidden_pop(motor_conn_i, width, length, True)
        for i in range(len(list_of_lists)):
            split_the_from_list(hidden_pops[i], motor_output, list_of_lists[i], receptor_type="inhibitory")
        # split_the_from_list(visual_input, hidden_pop, visual_connections[layer])
        # split_the_from_list(hidden_pop, motor_output, motor_conn_e)
        # split_the_from_list(hidden_pops[layer], motor_output, motor_conn_i, receptor_type="inhibitory")
        all_pops.append(hidden_pops)
    print "finished connecting"
    return all_pops

simulate = True

sim.setup(timestep=1.0)
# sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 255)

width = 2
length = 2

# mapping_1 = map_neurons_to_field(64, 19, 15, 0.9, 5)
mapping_2 = map_neurons_to_field(20, width, length, 0.9, 0)
# mapping_3 = map_neurons_to_field(50, 19, 15, 0.9, 2)
# mapping_4 = map_neurons_to_field(128, 2, 2, 0.9, 5)
# mapping_5 = map_neurons_to_field(128, 2, 2, 0.9, 7)
print "created mapping"
# connections_1 = map_to_from_list(mapping_1, 19, 15, 0.9)
connections_2 = map_to_from_list(mapping_2, width, length, 0.9)
# connections_3 = map_to_from_list(mapping_3, 19, 15, 0.9)
# connections_4 = map_to_from_list(mapping_4, 2, 2, 0.9)
# connections_5 = map_to_from_list(mapping_5, 2, 2, 0.9)
print "created all connections"


sim.setup(timestep=1.0)
# sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 32)

# set up populations,
if simulate:
    # Assuming channel 0 as left camera and channel 1 as right camera
    # Import data.log and Decode events
    dm = DataManager()
    dm.load_AE_from_yarp('acquisitions10042019/circle10042019')

    # Loading decoded events; data(timestamp, channel, x, y, polarity)
    stereo_data = np.loadtxt('acquisitions10042019/circle10042019/decoded_events.txt', delimiter=',')
    [left_data, right_data] = split_stereo_data(stereo_data)
    # left_data.tolist()
    # right_data.tolist()

    new_left = convert_data(left_data)
    new_right = convert_data(right_data)

    print('ATIS data processing ended')

    vis_pop = sim.Population(width*length, sim.SpikeSourceArray(new_left), label='pop_in')
else:
    vis_pop = sim.Population(None, ICUBInputVertex(spinnaker_link_id=0), label='pop_in')

pop_out = sim.Population(4, sim.IF_curr_exp(tau_refrac=3), label="motor_control")
if simulate:
    pop_out.record(['spikes', 'v'])

# pop_out = sim.Population(None, ICUBOutputVertex(spinnaker_link_id=0), label='pop_out')

# hidden_pops = connect_it_up(vis_pop, pop_out, connections_1, 19, 15)
hidden_pops = connect_it_up(vis_pop, pop_out, connections_2, width, length)
# connect_it_up(vis_pop, pop_out, connections_3, 19, 15)
# connect_it_up(vis_pop, pop_out, connections_4, 2, 2)
# connect_it_up(vis_pop, pop_out, connections_5, 2, 2)

# test_input = sim.Population(304*240, sim.IF_curr_exp(), label="readout")
# test_input.record(['spikes', 'v'])
# sim.Projection(vis_pop, test_input, sim.OneToOneConnector(), sim.StaticSynapse(weight=0.1))

# sim.Projection(pop, neuron_pop, sim.OneToOneConnector(), sim.StaticSynapse(weight=20.0))

sim.external_devices.activate_live_output_to(pop_out, vis_pop)

# out_port = yarp.BufferedPortBottle()
# out_port.open('/spinn:o')
# # bottle = out_port.prepare()
# # bottle.clear()
# # bottle.addInt32(2)
# # out_port.write()
# # out_port
# # b.addString("thing")
# while True:
#     bottle = out_port.prepare()
#     bottle.clear()
#     bottle.addInt32(2)
#     out_port.write()

#recordings and simulations,
#neuron_pop.record("spikes")

simtime = 30000 #ms,
if simulate:
    sim.run(simtime)
else:
    sim.external_devices.run_forever()
    raw_input('Press enter to stop')

# continuous run until key press
# remember: do NOT record when running in this mode

if simulate:
    exc_spikes = pop_out.get_data("spikes")
    exc_v = pop_out.get_data("v")
    hidden_spikes = []
    hidden_v = []
    for i in range(len(hidden_pops[0])):
        hidden_spikes.append(hidden_pops[0][i].get_data("spikes"))
        hidden_v.append(hidden_pops[0][i].get_data("v"))
    # input_spikes = test_input.get_data("spikes")
    # input_v = test_input.get_data("v")

    Figure(
        # raster plot of the neuron_pop
        Panel(exc_spikes.segments[0].spiketrains, xlabel="Time/ms", xticks=True,
              yticks=True, markersize=0.2, xlim=(0, simtime)),
        Panel(exc_v.segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        Panel(hidden_spikes[0].segments[0].spiketrains, xlabel="Time/ms", xticks=True,
              yticks=True, markersize=0.2, xlim=(0, simtime)),
        Panel(hidden_v[0].segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        Panel(hidden_spikes[1].segments[0].spiketrains, xlabel="Time/ms", xticks=True,
              yticks=True, markersize=0.2, xlim=(0, simtime)),
        Panel(hidden_v[1].segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        Panel(hidden_spikes[2].segments[0].spiketrains, xlabel="Time/ms", xticks=True,
              yticks=True, markersize=0.2, xlim=(0, simtime)),
        Panel(hidden_v[2].segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        Panel(hidden_spikes[3].segments[0].spiketrains, xlabel="Time/ms", xticks=True,
              yticks=True, markersize=0.2, xlim=(0, simtime)),
        Panel(hidden_v[3].segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        # Panel(input_spikes.segments[0].spiketrains, xlabel="Time/ms", xticks=True,
        #       yticks=True, markersize=0.2, xlim=(0, simtime)),
        # Panel(input_v.segments[0].filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
        title="neuron_pop: spikes"
    )
    plt.show()

sim.end()

print("finished")
