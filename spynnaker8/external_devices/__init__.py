"""
The :py:mod:`spynnaker.pynn` package contains the front end specifications
and implementation for the PyNN High-level API
(http://neuralensemble.org/trac/PyNN)
"""

import logging
import os

from spinn_front_end_common.abstract_models \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utility_models import LivePacketGather
from spinn_utilities.socket_address import SocketAddress
from spinnman.messages.eieio import EIEIOType

# main
from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
import spynnaker8

# components
from spynnaker8.external_device_models \
    import ArbitraryFPGADeviceDataHolder as ArbitraryFPGADevice
from spynnaker8.external_device_models \
    import ExternalCochleaDeviceDataHolder as ExternalCochleaDevice
from spynnaker8.external_device_models \
    import ExternalFPGARetinaDeviceDataHolder as ExternalFPGARetinaDevice
from spynnaker8.external_device_models \
    import MunichMotorDeviceDataHolder as MunichMotorDevice
from spynnaker8.external_device_models \
    import MunichRetinaDeviceDataHolder as MunichRetinaDevice

# injector for spynnaker 8
from spynnaker8.models.model_data_holders \
    import SpikeInjectorDataHolder as ExternalDeviceSpikeInjector

# connections
from spynnaker.pyNN import model_binaries
from spynnaker.pyNN.connections \
    import EthernetCommandConnection
from spynnaker.pyNN.connections \
    import EthernetControlConnection
from spynnaker.pyNN.connections \
    import SpynnakerLiveSpikesConnection

# abstract
from spynnaker.pyNN.external_devices_models \
    import AbstractEthernetController
from spynnaker.pyNN.external_devices_models \
    import AbstractEthernetSensor

# General LIF control
from spynnaker8.external_device_models\
    import ExternalDeviceLifControlDataHolder\
    as ExternalDeviceLifControl

# PushBot Ethernet model control
from spynnaker8.external_device_models.push_bot\
    .push_bot_control_models \
    import PushBotLifEthernetDataHolder as PushBotLifEthernet

# PushBot SpiNNakerLink control
from spynnaker8.external_device_models.push_bot\
    .push_bot_control_models \
    import PushBotLifSpinnakerLinkDataHolder as PushBotLifSpinnakerLink
from spynnaker8.external_device_models.push_bot.\
    push_bot_control_models import PushBotSpinnakerLinkRetinaDeviceDataHolder\
    as PushBotSpiNNakerLinkRetinaDevice

# push bot ethernet components
from spynnaker.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet import PushBotEthernetLaserDevice
from spynnaker.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet import PushBotEthernetLEDDevice
from spynnaker.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet import PushBotEthernetMotorDevice
from spynnaker.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet import PushBotEthernetRetinaDevice
from spynnaker.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet import PushBotEthernetSpeakerDevice
from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotLaser

# push bot parameters
from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotLED
from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotMotor
from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotRetinaResolution

# push bot retina viewer
from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotRetinaViewer

from spynnaker.pyNN.external_devices_models.push_bot. \
    push_bot_parameters import PushBotSpeaker

# push bot spinnaker link devices
from spynnaker.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link import PushBotSpiNNakerLinkLaserDevice
from spynnaker.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link import PushBotSpiNNakerLinkLEDDevice
from spynnaker.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link import PushBotSpiNNakerLinkMotorDevice
from spynnaker.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link import PushBotSpiNNakerLinkSpeakerDevice

# PushBot protocols
from spynnaker.pyNN.protocols import MunichIoSpiNNakerLinkProtocol

# main thing
from spynnaker.pyNN.spynnaker_external_device_plugin_manager \
    import SpynnakerExternalDevicePluginManager

# useful functions
add_database_socket_address = \
    SpynnakerExternalDevicePluginManager.add_database_socket_address
activate_live_output_to = \
    SpynnakerExternalDevicePluginManager.activate_live_output_to
activate_live_output_for = \
    SpynnakerExternalDevicePluginManager.activate_live_output_for

logger = logging.getLogger(__name__)

AbstractSpiNNakerCommon.register_binary_search_path(
    os.path.dirname(model_binaries.__file__))
spynnaker_external_devices = SpynnakerExternalDevicePluginManager()

__all__ = [
    "EIEIOType",

    # General Devices
    "ExternalCochleaDevice", "ExternalFPGARetinaDevice",
    "MunichRetinaDevice", "MunichMotorDevice",
    "ArbitraryFPGADevice", "PushBotRetinaViewer",

    # devices pynn 8
    "ExternalCochleaDevice", "ExternalFPGARetinaDevice",
    "MunichRetinaDevice", "MunichMotorDevice",
    "PushBotRetinaDevice", "ArbitraryFPGADevice",
    "ExternalDeviceLifControl",

    # Pushbot Parameters
    "MunichIoSpiNNakerLinkProtocol",
    "PushBotLaser", "PushBotLED", "PushBotMotor", "PushBotSpeaker",
    "PushBotRetinaResolution",

    # Pushbot Ethernet Parts
    "PushBotLifEthernet", "PushBotEthernetLaserDevice",
    "PushBotEthernetLEDDevice", "PushBotEthernetMotorDevice",
    "PushBotEthernetSpeakerDevice", "PushBotEthernetRetinaDevice",

    # Pushbot SpiNNaker Link Parts
    "PushBotLifSpinnakerLink", "PushBotSpiNNakerLinkLaserDevice",
    "PushBotSpiNNakerLinkLEDDevice", "PushBotSpiNNakerLinkMotorDevice",
    "PushBotSpiNNakerLinkSpeakerDevice", "PushBotSpiNNakerLinkRetinaDevice",

    # Connections
    "SpynnakerLiveSpikesConnection",

    # Provided functions
    "activate_live_output_for",
    "activate_live_output_to",
    "SpikeInjector",
    "register_database_notification_request"
]


def register_database_notification_request(hostname, notify_port, ack_port):
    """ Adds a socket system which is registered with the notification protocol

    :param hostname: hostname to connect to
    :param notify_port: port num for the notify command
    :param ack_port: port num for the ack command
    :rtype: None
    """
    spynnaker_external_devices.add_socket_address(
        SocketAddress(hostname, notify_port, ack_port))


def EthernetControlPopulation(
        n_neurons, model, label=None, local_host=None, local_port=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a PyNN population that can be included in a network to\
        control an external device which is connected to the host
    :param n_neurons: The number of neurons in the control population
    :param model: Class of a model that implements AbstractEthernetController
    :param label: An optional label for the population
    :param local_host:\
            The optional local host IP address to listen on for commands
    :param local_port: The optional local port to listen on for commands
    :param database_ack_port_num:\
            The optional port to which responses to the database notification\
            protocol are to be sent
    :param database_notify_port_num:\
            The optional port to which notifications from the database\
            notification protocol are to be sent
    :return:\
            A pyNN Population which can be used as the target of a Projection.\
            Note that the Population can also be used as the source of a\
            Projection, but it might not send spikes.
    """
    if not issubclass(model.build_model(), AbstractEthernetController):
        raise Exception(
            "Model must be a subclass of AbstractEthernetController")
    population = spynnaker8.Population(n_neurons, model, label=label)
    vertex = population._get_vertex
    translator = vertex.get_message_translator()
    ethernet_control_connection = EthernetControlConnection(
        translator, local_host, local_port)
    devices_with_commands = [
        device for device in vertex.get_external_devices()
        if isinstance(device, AbstractSendMeMulticastCommandsVertex)
    ]
    if len(devices_with_commands) > 0:
        ethernet_command_connection = EthernetCommandConnection(
            translator, devices_with_commands, local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    live_packet_gather = LivePacketGather(
        ethernet_control_connection.local_ip_address,
        ethernet_control_connection.local_port,
        message_type=EIEIOType.KEY_PAYLOAD_32_BIT,
        payload_as_time_stamps=False, use_payload_prefix=False)
    spynnaker_external_devices.add_application_vertex(live_packet_gather)
    for partition_id in vertex.get_outgoing_partition_ids():
        spynnaker_external_devices.add_edge(
            vertex, live_packet_gather, partition_id)
    return population


def EthernetSensorPopulation(
        device, local_host=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a pyNN population which can be included in a network to\
        receive spikes from a device connected to the host
    :param device: Class of a model that implements AbstractEthernetController
    :param local_host:\
            The optional local host IP address to listen on for database\
            notification
    :param database_ack_port_num:\
            The optional port to which responses to the database notification\
            protocol are to be sent
    :param database_notify_port_num:\
            The optional port to which notifications from the database\
            notification protocol are to be sent
    :return:\
            A pyNN Population which can be used as the source of a Projection.\
            Note that the Population cannot be used as the target of a\
            Projection.
    """
    if not isinstance(device, AbstractEthernetSensor):
        raise Exception("Model must be an instance of AbstractEthernetSensor")
    injector_params = dict(device.get_injector_parameters())
    injector_params['notify'] = False

    population = spynnaker8.Population(
        device.get_n_neurons(), SpikeInjector(**injector_params),
        label=device.get_injector_label())
    if isinstance(device, AbstractSendMeMulticastCommandsVertex):
        ethernet_command_connection = EthernetCommandConnection(
            device.get_translator(), [device], local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    database_connection = device.get_database_connection()
    if database_connection is not None:
        add_database_socket_address(
            database_connection.local_ip_address,
            database_connection.local_port, database_ack_port_num)
    return population


def SpikeInjector(
        label=None, port=None, notify=True, virtual_key=None,
        database_notify_host=None, database_notify_port_num=None,
        database_ack_port_num=None):
    """ Supports adding a spike injector to the application graph.

    :param n_neurons: the number of neurons the spike injector will emulate
    :type n_neurons: int
    :param label: the label given to the population
    :type label: str
    :param port: the port number used to listen for injections of spikes
    :type port: int
    :param virtual_key: the virtual key used in the routing system
    :type virtual_key: int
    :param database_notify_host: the hostname for the device which is\
            listening to the database notification.
    :type database_notify_host: str
    :param database_ack_port_num: the port number to which a external device\
            will acknowledge that they have finished reading the database and\
            are ready for it to start execution
    :type database_ack_port_num: int
    :param database_notify_port_num: The port number to which a external\
            device will receive the database is ready command
    :type database_notify_port_num: int
    """
    if notify:
        add_database_socket_address(database_notify_host,
                                    database_notify_port_num,
                                    database_ack_port_num)
    return ExternalDeviceSpikeInjector(
        label=label, port=port, virtual_key=virtual_key)
