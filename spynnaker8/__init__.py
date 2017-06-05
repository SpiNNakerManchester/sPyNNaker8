# common imports
import atexit

# pynn imports
from pyNN import common as pynn_common
from pyNN.common import control as pynn_control
from pyNN.recording import get_io
from pyNN.standardmodels import StandardCellType
from pyNN.random import NumpyRNG, RandomDistribution
from pyNN.space import \
    distance, Space, Line, Grid2D, Grid3D, Cuboid, Sphere, RandomStructure

# fec improts
from spinn_front_end_common.utilities import exceptions
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.failed_state import FAILED_STATE_MSG
from spinn_front_end_common.utilities.notification_protocol. \
    socket_address import SocketAddress

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

# Exceptions
from spynnaker8.utilities.exceptions import PyNN7Exception

import logging

logger = logging.getLogger(__name__)

__all__ = [
    # PyNN imports
    'Cuboid', 'distance', 'Grid2D', 'Grid3D', 'Line', 'NumpyRNG',
    'RandomDistribution', 'RandomStructure', 'Space', 'Sphere',

    # connections
    'AllToAllConnector', 'ArrayConnector', 'CSAConnector',
    'DistanceDependentProbabilityConnector', 'FixedNumberPostConnector',
    'FixedNumberPreConnector', 'FixedProbabilityConnector',
    'FromFileConnector', 'FromListConnector', 'IndexBasedProbabilityConnector',
    'MultapseConnector', 'OneToOneConnector', 'SmallWorldConnector',
    # synapse structures
    'StaticSynapse',
    # plastic stuff
    'STDPMechanism', 'AdditiveWeightDependence',
    'MultiplicativeWeightDependence', 'SpikePairRule',
    # neuron stuff
    'IF_cond_exp', 'IF_curr_duel_exp', 'IF_curr_exp', 'Izhikevich_cond',
    'Izhikevich', 'SpikeSourceArray', 'SpikeSourcePoisson',
    # pops
    'Assembly', 'Population', 'PopulationView',
    # projection
    'SpiNNakerProjection',

    # Stuff that we define
    'end', 'setup', 'run', 'run_until', 'run_for', 'num_processes', 'rank',
    'reset', 'set_number_of_neurons_per_core',
    'register_database_notification_request', 'Projection',
    'get_current_time', 'create', 'connect', 'get_time_step', 'get_min_delay',
    'get_max_delay', 'initialize', 'list_standard_models', 'name',
    'num_processes', 'record', 'record_v', 'record_gsyn']


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
    if globals_variables.has_simulator():
        # if already exists, kill and rebuild
        globals_variables.get_simulator().clear()

    # add default label if needed
    if graph_label is None:
        graph_label = "PyNN0.8_graph"

    # create the main object for all stuff related software
    SpiNNaker(
        database_socket_addresses=database_socket_addresses,
        extra_algorithm_xml_paths=extra_algorithm_xml_paths,
        extra_mapping_inputs=extra_mapping_inputs,
        extra_mapping_algorithms=extra_mapping_algorithms,
        extra_pre_run_algorithms=extra_pre_run_algorithms,
        extra_post_run_algorithms=extra_post_run_algorithms,
        extra_load_algorithms=extra_load_algorithms,
        time_scale_factor=time_scale_factor, timestep=timestep,
        min_delay=min_delay, max_delay=max_delay, graph_label=graph_label,
        n_chips_required=None)

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
    global __pynn_run, __pynn_run_until
    global __pynn_get_current_time, __pynn_get_time_step, __pynn_get_min_delay
    global __pynn_get_max_delay, __pynn_num_processes, __pynn_rank
    global __pynn_reset, __pynn_initialize, __pynn_create, __pynn_connect
    global __pynn_record

    # overload the failed ones with now valid ones, now that we're in setup
    # phase.
    __pynn_run, __pynn_run_until = pynn_common.build_run(spinnaker_simulator)

    tuple = pynn_common.build_state_queries(spinnaker_simulator)
    __pynn_get_current_time, __pynn_get_time_step, __pynn_get_min_delay, \
        __pynn_get_max_delay, __pynn_num_processes, __pynn_rank = tuple

    __pynn_reset = pynn_common.build_reset(spinnaker_simulator)
    __pynn_create = pynn_common.build_create(Population)

    __pynn_connect = pynn_common.build_connect(
        Projection, FixedProbabilityConnector, StaticSynapse)

    __pynn_record = pynn_common.build_record(spinnaker_simulator)


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


def record_v(source, filename):
    """ depreciated method for getting voltage
    this is not documented in the public facing api
    :param source: the population / view / assembly to record
    :param filename: the neo file to write to
    :return: None
    """
    logger.warn(
        "Using record_v is deprecated.  Use record('v') function instead")
    record(['v'], source, filename)


def record_gsyn(source, filename):
    """depreciated method for getting both types of gsyn
    this is not documented in the public facing api

    :param source: the population / view / assembly to record
    :param filename: the neo file to write to
    :return: None
    """

    logger.warn(
        "Using record_gsyn is deprecated.  Use record('gsyn_exc') and/or"
        " record('gsyn_inh') function instead")
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
    if globals_variables.has_simulator():
        globals_variables.get_simulator().stop()


def set_number_of_neurons_per_core(neuron_type, max_permitted):
    """ Sets a ceiling on the number of neurons of a given type that can be\
        placed on a single core.
    :param neuron_type:
    :param max_permitted:
    """
    try:
        simulator = globals_variables.get_simulator()
        simulator.set_number_of_neurons_per_core(neuron_type.build_model(),
                                                 max_permitted)
    except AttributeError as ex:
        if isinstance(neuron_type, str):
            msg = "set_number_of_neurons_per_core call now expects " \
                  "neuron_type as a class instead of as a str"
            raise PyNN7Exception(msg)
        raise ex


def register_database_notification_request(hostname, notify_port, ack_port):
    """ Adds a socket system which is registered with the notification protocol

    :param hostname:
    :param notify_port:
    :param ack_report:
    :return:
    """
    globals_variables.get_simulator().add_socket_address(
        SocketAddress(hostname, notify_port, ack_port))


# These methods will deffer to PyNN methods if a simulator exists


def connect(pre, post, weight=0.0, delay=None, receptor_type=None, p=1,
            rng=None):
    global __pynn_connect
    if globals_variables.has_simulator():
        __pynn_connect(pre, post, weight, delay, receptor_type, p, rng)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def create(cellclass, cellparams=None, n=1):
    global __pynn_create
    if globals_variables.has_simulator():
        __pynn_create(cellclass, cellparams, n)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def get_current_time():
    global __pynn_get_current_time
    if globals_variables.has_simulator():
        return __pynn_get_current_time()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def get_min_delay():
    global __pynn_get_min_delay
    if globals_variables.has_simulator():
        return __pynn_get_min_delay()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def get_max_delay():
    global __pynn_get_max_delay
    if globals_variables.has_simulator():
        return __pynn_get_max_delay()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def get_time_step():
    global __pynn_get_time_step
    if globals_variables.has_simulator():
        return __pynn_get_time_step()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def initialize(cells, **initial_values):
    if globals_variables.has_simulator():
        pynn_common.initialize(cells, **initial_values)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def num_processes():
    global __pynn_num_processes
    if globals_variables.has_simulator():
        return __pynn_num_processes()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def rank():
    global __pynn_rank
    if globals_variables.has_simulator():
        return __pynn_rank()
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def record(variables, source, filename, sampling_interval=None,
           annotations=None):
    global __pynn_record
    if globals_variables.has_simulator():
        return __pynn_record(variables, source, filename, sampling_interval,
                             annotations)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def reset(annotations={}):
    global __pynn_reset
    if globals_variables.has_simulator():
        __pynn_reset(annotations)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


def run(simtime, callbacks=None):
    global __pynn_run
    if globals_variables.has_simulator():
        return __pynn_run(simtime, callbacks=callbacks)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)


# left here becuase needs to be done, and no better place to put it
# (ABS dont like it, but will put up with it)
run_for = run


def run_until(self, tstop):
    global __pynn_run_until
    if globals_variables.has_simulator():
        return __pynn_run_until(tstop)
    else:
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)
