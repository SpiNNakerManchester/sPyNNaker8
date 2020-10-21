from pacman.model.constraints.key_allocator_constraints import (
    FixedKeyAndMaskConstraint)
from pacman.model.routing_info import BaseKeyAndMask
from spinn_front_end_common.utility_models import (
    ReverseIPTagMulticastSourceMachineVertex)
from spynnaker.pyNN.models.utility_models.delays import (
    DelayExtensionMachineVertex)


class KeyConstraintAdder(object):

    def __call__(self, machine_graph):
        for outgoing_partition in machine_graph.outgoing_edge_partitions:
            mac_vertex = outgoing_partition.pre_vertex
            if isinstance(mac_vertex, ReverseIPTagMulticastSourceMachineVertex):
                if mac_vertex.vertex_slice.lo_atom == 0:
                    outgoing_partition.add_constraint(
                        FixedKeyAndMaskConstraint(
                            [BaseKeyAndMask(base_key=0, mask=0xFFFFFFc0)]))
                else:
                    outgoing_partition.add_constraint(
                        FixedKeyAndMaskConstraint(
                            [BaseKeyAndMask(base_key=64, mask=0xFFFFFFc0)]))
            elif isinstance(mac_vertex, DelayExtensionMachineVertex):
                if mac_vertex.vertex_slice.lo_atom == 0:
                    outgoing_partition.add_constraint(
                        FixedKeyAndMaskConstraint(
                            [BaseKeyAndMask(base_key=128, mask=0xFFFFFFc0)]))
                else:
                    outgoing_partition.add_constraint(
                        FixedKeyAndMaskConstraint(
                            [BaseKeyAndMask(base_key=192, mask=0xFFFFFFc0)]))
