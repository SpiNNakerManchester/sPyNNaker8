# pynn imports
from pyNN.common import control as pynn_control

# spynnaker 8 imports
from spynnaker8 import _version

# common front end imports
from spinn_front_end_common.interface.spinnaker_main_interface import \
    SpinnakerMainInterface

# local stuff
from collections import defaultdict
from six import iteritems, itervalues
import logging
import itertools
import numpy
import math
import os

logger = logging.getLogger(__name__)


class SpiNNaker(SpinnakerMainInterface, pynn_control.BaseState):
    """ main interface for the stuff software for PyNN 0.8

    """

    def __init__(
            self, config, executable_finder, database_socket_addresses,
            extra_algorithm_xml_paths, extra_mapping_inputs,
            extra_mapping_algorithms, extra_pre_run_algorithms,
            extra_post_run_algorithms, extra_load_algorithms,
            time_scale_factor, min_delay, max_delay, graph_label,
            n_chips_required, timestep=0.1):

        # timing parameters
        self._min_delay = min_delay
        self._max_delay = max_delay

        # population and projection holders
        self._populations = list()
        self._projections = list()

        # config object
        self._config_parser = config

        # pynn demanded objects
        self._id_counter = 42
        self._segment_counter = -1
        self._name = "SpiNNaker_under_version({}-{})".format(
            _version.__version__, _version.__version_name__)
        self._recorders = set([])

        # main pynn interface inhirtence
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

        # spinnaker setup
        SpinnakerMainInterface.__init__(
            self, config=config, executable_finder=executable_finder,
            database_socket_addresses=database_socket_addresses,
            extra_algorithm_xml_paths=built_in_extra_xml_paths,
            extra_mapping_inputs=built_in_extra_mapping_inputs,
            extra_mapping_algorithms=extra_mapping_algorithms,
            extra_pre_run_algorithms=extra_pre_run_algorithms,
            extra_post_run_algorithms=extra_post_run_algorithms,
            extra_load_algorithms=built_in_extra_load_algorithms,
            graph_label=graph_label, n_chips_required=n_chips_required)

        self._machine_time_step = timestep
        self._time_scale_factor = time_scale_factor

        # Pass hostname to frontend
        self._set_up_timings(timestep, min_delay, max_delay)
        self.set_up_machine_specifics(None)

    def _set_up_timings(self, timestep, min_delay, max_delay):
        self._machine_time_step = config.getint("Machine", "machineTimeStep")

        # deal with params allowed via the setup options
        if timestep is not None:
            # convert into milliseconds from microseconds
            timestep *= 1000
            self._machine_time_step = timestep

        if min_delay is not None and float(min_delay * 1000) < 1.0 * timestep:
            raise common_exceptions.ConfigurationException(
                "Pacman does not support min delays below {} ms with the "
                "current machine time step"
                    .format(constants.MIN_SUPPORTED_DELAY * timestep))

        natively_supported_delay_for_models = \
            constants.MAX_SUPPORTED_DELAY_TICS
        delay_extension_max_supported_delay = \
            constants.MAX_DELAY_BLOCKS \
            * constants.MAX_TIMER_TICS_SUPPORTED_PER_BLOCK

        max_delay_tics_supported = \
            natively_supported_delay_for_models + \
            delay_extension_max_supported_delay

        if max_delay is not None \
                and float(
                            max_delay * 1000) > max_delay_tics_supported * timestep:
            raise common_exceptions.ConfigurationException(
                "Pacman does not support max delays above {} ms with the "
                "current machine time step".format(0.144 * timestep))
        if min_delay is not None:
            self._min_supported_delay = min_delay
        else:
            self._min_supported_delay = timestep / 1000.0

        if max_delay is not None:
            self._max_supported_delay = max_delay
        else:
            self._max_supported_delay = (max_delay_tics_supported *
                                         (timestep / 1000.0))

        if (config.has_option("Machine", "timeScaleFactor") and
                    config.get("Machine", "timeScaleFactor") != "None"):
            self._time_scale_factor = \
                config.getint("Machine", "timeScaleFactor")
            if timestep * self._time_scale_factor < 1000:
                if config.getboolean(
                        "Mode", "violate_1ms_wall_clock_restriction"):
                    logger.warn(
                        "****************************************************")
                    logger.warn(
                        "*** The combination of simulation time step and  ***")
                    logger.warn(
                        "*** the machine time scale factor results in a   ***")
                    logger.warn(
                        "*** wall clock timer tick that is currently not  ***")
                    logger.warn(
                        "*** reliably supported by the spinnaker machine. ***")
                    logger.warn(
                        "****************************************************")
                else:
                    raise common_exceptions.ConfigurationException(
                        "The combination of simulation time step and the"
                        " machine time scale factor results in a wall clock "
                        "timer tick that is currently not reliably supported "
                        "by the spinnaker machine.  If you would like to "
                        "override this behaviour (at your own risk), please "
                        "add violate_1ms_wall_clock_restriction = True to the "
                        "[Mode] section of your .spynnaker.cfg file")
        else:
            self._time_scale_factor = max(1,
                                          math.ceil(1000.0 / float(timestep)))
            if self._time_scale_factor > 1:
                logger.warn("A timestep was entered that has forced sPyNNaker "
                            "to automatically slow the simulation down from "
                            "real time by a factor of {}. To remove this "
                            "automatic behaviour, please enter a "
                            "timescaleFactor value in your .spynnaker.cfg"
                            .format(self._time_scale_factor))

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
        self._run(tstop - self._current_run_timesteps)

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

        self._segment_counter = -1

        SpinnakerMainInterface.reset(self)

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

        SpinnakerMainInterface.run(self, duration_ms)

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
        """ pointless method in stuff

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
        return self._current_run_timesteps

    @t.setter
    def t(self, new_value):
        """ new current run timesteps

        :param new_value: new value for current run timesteps
        :return: None
        """
        self._current_run_timesteps = new_value

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
    def min_delay(self):
        """ property for min delay, currently used by the synapse impl.
        can likely be gotten rid of

        :return:
        """
        return self._min_delay

    @property
    def max_delay(self):
        """ property for max delay, currently used by the synapse impl.
        can likely be gotten rid of

        :return:
        """
        return self._max_delay

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
        return self._name

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
