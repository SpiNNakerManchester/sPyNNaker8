# common imports
import atexit
import deprecation

# pynn imports
from pyNN import common as pynn_common
from pyNN.common import control as pynn_control
from pyNN.random import *
from pyNN.recording import *
from pyNN.standardmodels import StandardCellType

# fec improts
from spinn_front_end_common.utilities.notification_protocol. \
    socket_address import SocketAddress
from spinn_front_end_common.utilities import helpful_functions

# spynnaker imports
from spynnaker.pyNN.utilities import globals_variables
from spynnaker.pyNN.utilities.failed_state import FailedState

# connections
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.all_to_all_connector import \
    AllToAllConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.array_connector import ArrayConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.csa_connector import CSAConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.distance_dependent_probability_connector \
    import DistanceDependentProbabilityConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.fixed_number_post_connector import \
    FixedNumberPostConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.fixed_number_pre_connector import \
    FixedNumberPreConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.fixed_probability_connector import \
    FixedProbabilityConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.from_file_connector import FromFileConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.from_list_connector import FromListConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.index_based_probability_connector import\
    IndexBasedProbabilityConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.multapse_connector import MultapseConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.one_to_one_connector import \
    OneToOneConnector
# noinspection PyUnresolvedReferences
from spynnaker8.models.connectors.small_world_connector import \
    SmallWorldConnector

# synapse structures
from spynnaker8.models.synapse_dynamics.synapse_dynamics_static import \
    SynapseDynamicsStatic as StaticSynapse

# plastic stuff
from spynnaker8.models.synapse_dynamics.synapse_dynamics_stdp import \
    SynapseDynamicsSTDP as STDPMechanism
from spynnaker8.models.synapse_dynamics.weight_dependence\
    .weight_dependence_additive import WeightDependenceAdditive as \
    AdditiveWeightDependence
from spynnaker8.models.synapse_dynamics.weight_dependence\
    .weight_dependence_multiplicative import \
    WeightDependenceMultiplicative as MultiplicativeWeightDependence
from spynnaker8.models.synapse_dynamics.timing_dependence\
    .timing_dependence_spike_pair import TimingDependenceSpikePair as \
    SpikePairRule

# neuron stuff
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.if_cond_exp_data_holder import \
    IFCondExpDataHolder as IF_cond_exp
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.if_curr_dual_exp_data_holder \
    import IFCurrDualExpDataHolder as IF_curr_duel_exp
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.if_curr_exp_data_holder import \
    IFCurrExpDataHolder as IF_curr_exp
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.izk_cond_exp_data_holder import \
    IzkCondExpDataHolder as Izhikevich_cond
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.izk_curr_exp_data_holder import \
    IzkCurrExpDataHolder as Izhikevich
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.spike_source_array_data_holder \
    import SpikeSourceArrayDataHolder as SpikeSourceArray
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.spike_source_poisson_data_holder \
    import SpikeSourcePoissonDataHolder as SpikeSourcePoisson

# pops
# noinspection PyUnresolvedReferences
from spynnaker8.models.populations.assembly import Assembly
# noinspection PyUnresolvedReferences
from spynnaker8.models.populations.population import Population
# noinspection PyUnresolvedReferences
from spynnaker8.models.populations.population_view import PopulationView

# projection
# noinspection PyUnresolvedReferences
from spynnaker8.models.projection import Projection as SpiNNakerProjection

# big stuff
from spynnaker8.spinnaker import SpiNNaker
from spynnaker8.utilities import config
from spynnaker8._version import __version__

import logging
import os

logger = logging.getLogger(__name__)

# static methods that are expected from the top level PyNN interface.
# as these are currently invalid till setup, they are encapsulated as failure
# functions
run = FailedState.run
run_until = FailedState.run_until
run_for = FailedState.run_for
get_current_time = FailedState.get_current_time
get_time_step = FailedState.get_time_step
get_min_delay = FailedState.get_min_delay
get_max_delay = FailedState.get_max_delay
num_processes = FailedState.num_processes
rank = FailedState.rank
initialize = FailedState.initialize
reset = FailedState.reset
create = FailedState.create
connect = FailedState.connect

# this function is not documented in the public facing api
record = FailedState.record


def setup(timestep=pynn_control.DEFAULT_TIMESTEP,
          min_delay=pynn_control.DEFAULT_MIN_DELAY,
          max_delay=pynn_control.DEFAULT_MAX_DELAY,
          graph_label=None,
          database_socket_addresses=None, extra_algorithm_xml_paths=None,
          extra_mapping_inputs=None, extra_mapping_algorithms=None,
          extra_pre_run_algorithms=None, extra_post_run_algorithms=None,
          extra_load_algorithms=None, time_scale_factor=None, **extra_params):
    """ main method needed to be called to make the PyNN 0.8 setup. Needs to
    be called before any other function

    :param timestep:  the time step of the simulations
    :param min_delay: the min delay of the simulation
    :param max_delay: the max delay of the simulation
    :param graph_label: the label for the graph
    :param database_socket_addresses: the sockets used by external devices
    for the database notification protocol
    :param extra_algorithm_xml_paths: list of paths to where other xml are
    located
    :param extra_mapping_inputs: other inputs used by the mapping process
    :param extra_mapping_algorithms: other algorithms to be used by the
    mapping process
    :param extra_pre_run_algorithms: extra algorithms to use before a run
    :param extra_post_run_algorithms: extra algorithms to use after a run
    :param extra_load_algorithms: extra algorithms to use within the loading
    phase
    :param time_scale_factor: multiplicative factor to the machine time step
    (does not affect the neuron models accuracy)
    :param extra_params:  other stuff
    :return: rank thing
    """

    # setup PyNN common stuff
    pynn_common.setup(timestep, min_delay, max_delay, **extra_params)

    # create stuff simulator
    if not isinstance(globals_variables.get_simulator(),
                      FailedState):  # if already exists, kill and rebuild
        globals_variables.get_simulator().clear()

    # Rad config file
    config_parser = config.read_config()

    # add default label if needed
    if graph_label is None:
        graph_label = "PyNN0.8_graph"

    if time_scale_factor is None:
        time_scale_factor = helpful_functions.read_config_int(
            config_parser, "Machine", "timeScaleFactor")

    # create the main object for all stuff related software
    globals_variables.set_simulator(SpiNNaker(
        config=config_parser,
        database_socket_addresses=database_socket_addresses,
        extra_algorithm_xml_paths=extra_algorithm_xml_paths,
        extra_mapping_inputs=extra_mapping_inputs,
        extra_mapping_algorithms=extra_mapping_algorithms,
        extra_pre_run_algorithms=extra_pre_run_algorithms,
        extra_post_run_algorithms=extra_post_run_algorithms,
        extra_load_algorithms=extra_load_algorithms,
        time_scale_factor=time_scale_factor, timestep=timestep,
        min_delay=min_delay, max_delay=max_delay, graph_label=graph_label,
        n_chips_required=None))

    # warn about kwargs arguments
    if len(extra_params) > 0:
        logger.warn("Extra params {} have been applied to the setup "
                    "command which we do not consider".format(extra_params))

    # get overloaded functions from PyNN in relation of our simulator object
    _create_overloaded_functions(globals_variables.get_simulator())

    return rank()


def name():
    """ returns the name of the simulator

    :return:
    """
    return globals_variables.get_simulator().name


def Projection(
        presynaptic_population, postsynaptic_population,
        connector, synapse_type=None, source=None, receptor_type="excitatory",
        space=None, label=None):
    """ used to support pep 8 spelling correctly

    :param presynaptic_population: the source pop
    :param postsynaptic_population: the dest pop
    :param connector: the connector type
    :param synapse_type: the synapse type
    :param source: the source
    :param receptor_type: the recpetor type
    :param space: the space object
    :param label: the label
    :return:  a projection object for SpiNNaker
    """

    return SpiNNakerProjection(
        pre_synaptic_population=presynaptic_population,
        post_synaptic_population=postsynaptic_population, connector=connector,
        synapse_type=synapse_type, source=source, receptor_type=receptor_type,
        space=space, label=label)


def _create_overloaded_functions(spinnaker_simulator):
    """ creates functions that the main PyNN interface supports (
    given from PyNN)
    :param spinnaker_simulator: the simulator object we use underneath
    :return: None
    """

    # get the global functions
    global run, run_until, run_for, get_current_time, get_time_step, \
        get_min_delay, get_max_delay, num_processes, rank, reset, \
        initialize, create, connect, record

    # overload the failed ones with now valid ones, now that we're in setup
    # phase.
    run, run_until = pynn_common.build_run(spinnaker_simulator)
    run_for = run

    get_current_time, get_time_step, get_min_delay, get_max_delay, \
    num_processes, rank = pynn_common.build_state_queries(
        spinnaker_simulator)

    reset = pynn_common.build_reset(spinnaker_simulator)
    initialize = pynn_common.initialize
    create = pynn_common.build_create(Population)

    connect = pynn_common.build_connect(
        Projection, FixedProbabilityConnector, StaticSynapse)

    record = pynn_common.build_record(spinnaker_simulator)


def end(_=True):
    """ cleans up the spinnaker machine and software

    :param _: was named compatible_output, which we dont care about,
    so is a none existent parameter
    :return:  None
    """
    for (population, variables, filename) in \
            globals_variables.get_simulator().write_on_end:
        io = get_io(filename)
        population.write_data(io, variables)
    globals_variables.get_simulator().write_on_end = []
    globals_variables.get_simulator().stop()


@deprecation.deprecated(
    deprecated_in="1.0.0", current_version=__version__,
    details="Use record('v') function instead")
def record_v(source, filename):
    """ depreciated method for getting voltage
    this is not documented in the public facing api
    :param source: the population / view / assembly to record
    :param filename: the neo file to write to
    :return: None
    """
    record(['v'], source, filename)


@deprecation.deprecated(
    deprecated_in="1.0.0", current_version=__version__,
    details="Use record('gsyn_exc', 'gsyn_inh') function instead")
def record_gsyn(source, filename):
    """depreciated method for getting both types of gsyn
    this is not documented in the public facing api
    
    :param source: the population / view / assembly to record
    :param filename: the neo file to write to
    :return: None
    """
    record(['gsyn_exc', 'gsyn_inh'], source, filename)


def list_standard_models():
    """Return a list of all the StandardCellType
    classes available for this simulator."""
    return [obj.__name__
            for obj in globals().values()
            if isinstance(obj, type) and issubclass(obj, StandardCellType)]


@atexit.register
def _stop_on_spinnaker():
    # Stop SpiNNaker simulation
    if not isinstance(globals_variables.get_simulator(), FailedState):
        globals_variables.get_simulator().stop()


def set_number_of_neurons_per_core(neuron_type, max_permitted):
    """ Sets a ceiling on the number of neurons of a given type that can be\
        placed on a single core.
    :param neuron_type:
    :param max_permitted:
    """

    if hasattr(neuron_type.build_model(), "set_model_max_atoms_per_core"):
        neuron_type.build_model().set_model_max_atoms_per_core(max_permitted)
    else:
        raise Exception("{} is not a Vertex type"
                        .format(neuron_type))


def register_database_notification_request(hostname, notify_port, ack_port):
    """ Adds a socket system which is registered with the notification protocol

    :param hostname:
    :param notify_port:
    :param ack_report:
    :return:
    """
    globals_variables.get_simulator()._add_socket_address(
        SocketAddress(hostname, notify_port, ack_port))
