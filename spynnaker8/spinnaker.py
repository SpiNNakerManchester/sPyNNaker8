# pynn imports
from pyNN.common import control as pynn_control
from pyNN.random import RandomDistribution, NumpyRNG
from pyNN import __version__ as pynn_version

from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon

from spynnaker8 import _version
from spynnaker8.spynnaker8_simulator_interface \
    import Spynnaker8SimulatorInterface
from spynnaker8.utilities.spynnaker8_failed_state import Spynnaker8FailedState
from spynnaker8.utilities.random_stats import RandomStatsExponentialImpl
from spynnaker8.utilities.random_stats import RandomStatsGammaImpl
from spynnaker8.utilities.random_stats import RandomStatsLogNormalImpl
from spynnaker8.utilities.random_stats import RandomStatsNormalClippedImpl
from spynnaker8.utilities.random_stats import RandomStatsNormalImpl
from spynnaker8.utilities.random_stats import RandomStatsPoissonImpl
from spynnaker8.utilities.random_stats import RandomStatsRandIntImpl
from spynnaker8.utilities.random_stats import RandomStatsUniformImpl
from spynnaker8.utilities.random_stats import RandomStatsVonmisesImpl
from spynnaker8.utilities.random_stats import RandomStatsBinomialImpl
from _version import __version__ as version

import logging
import math

from quantities import __version__ as quantities_version
from neo import __version__ as neo_version
from lazyarray import __version__ as lazyarray_version


logger = logging.getLogger(__name__)

# At import time change the default FailedState
globals_variables.set_failed_state(Spynnaker8FailedState())

NAME = "SpiNNaker_under_version({}-{})".format(
            _version.__version__, _version.__version_name__)


class SpiNNaker(AbstractSpiNNakerCommon, pynn_control.BaseState,
                Spynnaker8SimulatorInterface):
    """ main interface for the stuff software for PyNN 0.8

    """

    def __init__(
            self, database_socket_addresses,
            extra_algorithm_xml_paths, extra_mapping_inputs,
            extra_mapping_algorithms, extra_pre_run_algorithms,
            extra_post_run_algorithms, extra_load_algorithms,
            time_scale_factor, min_delay, max_delay, graph_label,
            n_chips_required, timestep=0.1, hostname=None):

        # change min delay auto to be the min delay supported by simulator
        if min_delay == "auto":
            min_delay = timestep

        # population and projection holders
        self._populations = list()
        self._projections = list()

        # pynn demanded objects
        self._id_counter = 42
        self._segment_counter = 0
        self._recorders = set([])

        # main pynn interface inheritance
        pynn_control.BaseState.__init__(self)

        # handle the extra load algorithms and the built in ones
        built_in_extra_load_algorithms = list()

        if extra_load_algorithms is not None:
            built_in_extra_load_algorithms.extend(extra_load_algorithms)

        # handle extra xmls and the ones needed by default
        built_in_extra_xml_paths = list()

        if extra_algorithm_xml_paths is not None:
            built_in_extra_xml_paths.extend(extra_algorithm_xml_paths)

        # handle the extra mapping inputs and the built in ones
        built_in_extra_mapping_inputs = dict()

        if extra_mapping_inputs is not None:
            built_in_extra_mapping_inputs.update(
                built_in_extra_mapping_inputs)

        front_end_versions = [("sPyNNaker8_version", version)]
        front_end_versions.append(("pyNN_version", pynn_version))
        front_end_versions.append(("quantities_version", quantities_version))
        front_end_versions.append(("neo_version", neo_version))
        front_end_versions.append(("lazyarray_version", lazyarray_version))

        # spinnaker setup
        AbstractSpiNNakerCommon.__init__(
            self, database_socket_addresses=database_socket_addresses,
            user_extra_algorithm_xml_path=built_in_extra_xml_paths,
            user_extra_mapping_inputs=built_in_extra_mapping_inputs,
            extra_mapping_algorithms=extra_mapping_algorithms,
            user_extra_algorithms_pre_run=extra_pre_run_algorithms,
            extra_post_run_algorithms=extra_post_run_algorithms,
            extra_load_algorithms=built_in_extra_load_algorithms,
            graph_label=graph_label, n_chips_required=n_chips_required,
            hostname=hostname, min_delay=min_delay,
            max_delay=max_delay, timestep=timestep,
            time_scale_factor=time_scale_factor,
            front_end_versions=front_end_versions)

    def run(self, simtime):
        """ PyNN run simulation (enforced method and parameter name)

        :param simtime: the runtime in milliseconds
        :return: None
        """

        self._run(simtime)

    def run_until(self, tstop):
        """ functions demanded by pynn level api

        :param tstop: when to run until in milliseconds
        :return: None
        """
        # Build data
        self._run(tstop - self.t)

    def clear(self):
        """ whats clear vs reset??????????

        :return: None
        """
        self.recorders = set([])
        self._id_counter = 42
        self._segment_counter = -1
        self.reset()

        # Stop any currently running SpiNNaker application
        self.stop()

    def reset(self):
        """Reset the state of the current network to time t = 0.

        :return: None
        """
        for population in self._populations:
            population.cache_data()

        self._segment_counter += 1

        AbstractSpiNNakerCommon.reset(self)

    def _run(self, duration_ms):
        """ main interface for the starting of stuff

        :param duration_ms:
        :return:
        """

        # Convert dt into microseconds and divide by
        # realtime proportion to get hardware timestep
        hardware_timestep_us = int(round((1000.0 * float(self.dt)) /
                                         float(self.timescale_factor)))

        # Determine how long simulation is in timesteps
        duration_timesteps = \
            int(math.ceil(float(duration_ms) / float(self.dt)))

        logger.info("Simulating for %u %fms timesteps "
                    "using a hardware timestep of %uus",
                    duration_timesteps, self.dt, hardware_timestep_us)

        AbstractSpiNNakerCommon.run(self, duration_ms)

    @property
    def state(self):
        """ used to bypass the stupid duel level object

        :return: the stuff object
        """

        return self

    @property
    def mpi_rank(self):
        """ method demanded by PyNN due to MPI assumptions

        :return: ??????????
        """
        return 0

    @mpi_rank.setter
    def mpi_rank(self, new_value):
        """ this has no point in stuff

        :param new_value: pointless entry
        :return:
        """
        pass

    @property
    def num_processes(self):
        """ method demanded by PyNN due to MPI assumptions

        :return: ???????
        """
        return 1

    @num_processes.setter
    def num_processes(self, new_value):
        """ pointless method in stuff but needed for pynn interface

        :param new_value: pointless entry
        :return:
        """
        pass

    @property
    def dt(self):
        """ method demanded by PyNN due to api assumptions

        :return: the machine time step
        """

        return self._machine_time_step

    @dt.setter
    def dt(self, new_value):
        """ setter for the machine time step (forced by PyNN)

        :param new_value: new value for machine time step
        :return: None
        """
        self._machine_time_step = new_value

    @property
    def t(self):
        """ method demanded by PyNN due to api assumptions

        :return: the current runtime already executed
        """
        return (
            float(self._current_run_timesteps) *
            (float(self._machine_time_step) / 1000.0))

    @property
    def segment_counter(self):
        """ method demanded by the PyNN due to api assumptions

        :return: the segment counter ??????
        """
        return self._segment_counter

    @segment_counter.setter
    def segment_counter(self, new_value):
        """ method demanded by the PyNN due to api assumptions

        :param new_value: new value for the segment counter
        :return: None
        """
        self._segment_counter = new_value

    @property
    def id_counter(self):
        """ property for id_counter, currently used by the populations.
        (maybe it could live in the pop class???)

        :return:
        """
        return self._id_counter

    @id_counter.setter
    def id_counter(self, new_value):
        """ setter for id_counter, currently used by the populations.
        (maybe it could live in the pop class???)

        :param new_value: new value for id_counter
        :return:
        """
        self._id_counter = new_value

    @property
    def running(self):
        """ property method required from the base state object (ties into
        our has_ran parameter for auto pause and resume

        :return: the has_ran variable from the spinnaker main interface
        """
        return self._has_ran

    @running.setter
    def running(self, new_value):
        """ setter for the has_ran parameter, only used by the pynn interface,
        supports tracking where it thinks its setting this parameter.

        :param new_value: the new value for the simulation
        :return: None
        """
        self._has_ran = new_value

    @property
    def name(self):
        """ interface function needed to ensure pynn recoridng neo blocks are
        correctly labelled.

        :return: the name of the simulator.
        """
        return NAME

    @property
    def populations(self):
        """ property for the population list. needed by the population class.

        :return:
        """
        return self._populations

    @property
    def projections(self):
        """ property for the projections list. needed by the projection class.

        :return:
        """
        return self._projections

    @property
    def recorders(self):
        """ property method for the recorders, used by the pynn state object

        :return: the internal recorders object
        """
        return self._recorders

    @recorders.setter
    def recorders(self, new_value):
        """ setter for the internal recorders object

        :param new_value: the new value for the recorder
        :return:  None
        """
        self._recorders = new_value

    def get_distribution_to_stats(self):
        return {
            'binomial': RandomStatsBinomialImpl(),
            'gamma': RandomStatsGammaImpl(),
            'exponential': RandomStatsExponentialImpl(),
            'lognormal': RandomStatsLogNormalImpl(),
            'normal': RandomStatsNormalImpl(),
            'normal_clipped': RandomStatsNormalClippedImpl(),
            'poisson': RandomStatsPoissonImpl(),
            'uniform': RandomStatsUniformImpl(),
            'randint': RandomStatsRandIntImpl(),
            'vonmises': RandomStatsVonmisesImpl()}

    def get_random_distribution(self):
        return RandomDistribution

    def is_a_pynn_random(self, thing):
        return isinstance(thing, RandomDistribution)

    def get_pynn_NumpyRNG(self):
        return NumpyRNG()
