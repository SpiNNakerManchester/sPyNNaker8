# common imports
import numpy as __numpy

# pynn imports
from pyNN import common as pynn_common
from pyNN.common import control as pynn_control
from pyNN.recording import get_io
from pyNN.random import NumpyRNG, RandomDistribution
from pyNN.space import \
    distance, Space, Line, Grid2D, Grid3D, Cuboid, Sphere, RandomStructure

# fec imports
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.failed_state import FAILED_STATE_MSG

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
from spynnaker8.models.connectors.multapse_connector import MultapseConnector \
    as FixedTotalNumberConnector
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
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker8.models.model_data_holders.if_cond_exp_data_holder import \
    IFCondExpDataHolder as IF_cond_exp
# noinspection PyUnresolvedReferences
from spynnaker8.models.model_data_holders.if_curr_exp_data_holder import \
    IFCurrExpDataHolder as IF_curr_exp
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

from spynnaker8 import external_devices
from spynnaker8 import extra_models

# big stuff
from spynnaker8.spinnaker import SpiNNaker

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
    'FixedTotalNumberConnector', 'OneToOneConnector', 'SmallWorldConnector',
    # synapse structures
    'StaticSynapse',
    # plastic stuff
    'STDPMechanism', 'AdditiveWeightDependence',
    'MultiplicativeWeightDependence', 'SpikePairRule',
    # neuron stuff
    'IF_cond_exp', 'IF_curr_exp',
    'Izhikevich', 'SpikeSourceArray', 'SpikeSourcePoisson',
    # pops
    'Assembly', 'Population', 'PopulationView',
    # projection
    'SpiNNakerProjection',
    # External devices and extra models
    'external_devices', 'extra_models',
    # Stuff that we define
    'end', 'setup', 'run', 'run_until', 'run_for', 'num_processes', 'rank',
    'reset', 'set_number_of_neurons_per_core',
    'Projection',
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
          extra_load_algorithms=None, time_scale_factor=None,
          n_chips_required=None, **extra_params):
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
    :param n_chips_required: The number of chips needed by the simulation
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
        n_chips_required=n_chips_required)

    # warn about kwargs arguments
    if len(extra_params) > 0:
        logger.warn("Extra params {} have been applied to the setup "
                    "command which we do not consider".format(extra_params))

    # get overloaded functions from PyNN in relation of our simulator object
    _create_overloaded_functions(globals_variables.get_simulator())

    return rank()


def name():
    """ returns the name of the simulator

    :rtype:None
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
    :rtype: None
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
    :rtype:  None
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
    :rtype: None
    """
    logger.warn(
        "Using record_v is deprecated.  Use record('v') function instead")
    record(['v'], source, filename)


def record_gsyn(source, filename):
    """depreciated method for getting both types of gsyn
    this is not documented in the public facing api

    :param source: the population / view / assembly to record
    :param filename: the neo file to write to
    :rtype: None
    """

    logger.warn(
        "Using record_gsyn is deprecated.  Use record('gsyn_exc') and/or"
        " record('gsyn_inh') function instead")
    record(['gsyn_exc', 'gsyn_inh'], source, filename)


def list_standard_models():
    """Return a list of all the StandardCellType
    classes available for this simulator."""
    results = list()
    for (key, obj) in globals().iteritems():
        if isinstance(obj, type) and issubclass(obj, DataHolder)  \
                and not obj == DataHolder:
            results.append(key)
    return results


def set_number_of_neurons_per_core(neuron_type, max_permitted):
    """ Sets a ceiling on the number of neurons of a given type that can be\
        placed on a single core.
    :param neuron_type: neuron type
    :param max_permitted: the number to set to
    :rtype: None
    """
    if isinstance(neuron_type, str):
        msg = "set_number_of_neurons_per_core call now expects " \
              "neuron_typeas a class instead of as a str"
        raise ConfigurationException(msg)
    simulator = globals_variables.get_simulator()
    simulator.set_number_of_neurons_per_core(neuron_type.build_model(),
                                             max_permitted)


# These methods will deffer to PyNN methods if a simulator exists


def connect(pre, post, weight=0.0, delay=None, receptor_type=None, p=1,
            rng=None):
    """ builds a projection

    :param pre: source pop
    :param post: destination pop
    :param weight: weight of the connections
    :param delay: the delay of the connections
    :param receptor_type: excititory / inhib
    :param p: probability
    :param rng: random number generator
    :rtype: None
    """
    global __pynn_connect
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    __pynn_connect(pre, post, weight, delay, receptor_type, p, rng)


def create(cellclass, cellparams=None, n=1):
    """ builds a population with certian params

    :param cellclass: population class
    :param cellparams: population params.
    :param n: n neurons
    :rtype: None
    """
    global __pynn_create
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    __pynn_create(cellclass, cellparams, n)


def NativeRNG(seed_value):
    """ Fixes the random number generator's seed
    :param seed_value:
    :rtype: None
    """
    __numpy.random.seed(seed_value)


def get_current_time():
    """ the time within the simulation

    :return: returns the current time
    """
    global __pynn_get_current_time
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_get_current_time()


def get_min_delay():
    """the minimum allowed synaptic delay

    :return: returns the min delay of the simulation
    """
    global __pynn_get_min_delay
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_get_min_delay()


def get_max_delay():
    """ the maximum allowed synaptic delay

    :return: returns the max delay of the simulation
    """
    global __pynn_get_max_delay
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_get_max_delay()


def get_time_step():
    """ the integration time step

    :return: get the time step of the simulation
    """
    global __pynn_get_time_step
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_get_time_step()


def initialize(cells, **initial_values):
    """ sets cells values to certain values

    :param cells: the cells to change params on
    :param initial_values: the params and there values to change
    :rtype: None
    """
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    pynn_common.initialize(cells, **initial_values)


def num_processes():
    """the number of MPI processes

    :return: the num MPI processes
    """
    global __pynn_num_processes
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_num_processes()


def rank():
    """the MPI rank of the current node

    :return: mpi rank
    """
    global __pynn_rank
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_rank()


def record(variables, source, filename, sampling_interval=None,
           annotations=None):
    """ sets variables to be recorded

    :param variables: may be either a single variable name or a list of \
        variable names. For a given celltype class, celltype.recordable \
        contains a list of variables that can be recorded for that celltype.
    :param source: ?????
    :param filename: file name to write data to
    :param sampling_interval: how often to sample the reocrding, not \
        ignored so far
    :param annotations: the annotations to data writers
    :return: neo object
    """
    global __pynn_record
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_record(variables, source, filename, sampling_interval,
                         annotations)


def reset(annotations=None):
    """ resets the simulation to t = 0

    :param annotations: the annotations to the data objects
    :rtype: None
    """
    if annotations is None:
        annotations = {}
    global __pynn_reset
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    __pynn_reset(annotations)


def run(simtime, callbacks=None):
    """ The run() function advances the simulation for a given number of \
        milliseconds, e.g.:

    :param simtime:  time in milliseconds
    :param callbacks: callbacks to run
    :return: ?????
    """
    global __pynn_run
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_run(simtime, callbacks=callbacks)


# left here becuase needs to be done, and no better place to put it
# (ABS dont like it, but will put up with it)
run_for = run


def run_until(self, tstop):
    """ run until that time period has completed

    :param self: ????
    :param tstop: the time to stop at
    :return: ??????
    """
    global __pynn_run_until
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return __pynn_run_until(tstop)


def get_machine():
    """ Get the spinnaker machine in use
    :return: the machine object
    """
    if not globals_variables.has_simulator():
        raise ConfigurationException(FAILED_STATE_MSG)
    return globals_variables.get_simulator().machine
