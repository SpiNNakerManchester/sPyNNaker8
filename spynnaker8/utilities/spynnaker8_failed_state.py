from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities.failed_state import FAILED_STATE_MSG
from spynnaker.pyNN.utilities.spynnaker_failed_state \
    import SpynnakerFailedState
from spynnaker8.spynnaker8_simulator_interface \
    import Spynnaker8SimulatorInterface
import spynnaker8.spinnaker


class Spynnaker8FailedState(Spynnaker8SimulatorInterface,
                            SpynnakerFailedState, object):

    __slots__ = ()

    @property
    def dt(self):
        raise ConfigurationException(FAILED_STATE_MSG)

    @property
    def mpi_rank(self):
        raise ConfigurationException(FAILED_STATE_MSG)

    @property
    def name(self):
        return spynnaker8.spinnaker.NAME

    @property
    def num_processes(self):
        raise ConfigurationException(FAILED_STATE_MSG)

    @property
    def recorders(self):
        raise ConfigurationException(FAILED_STATE_MSG)

    @property
    def segment_counter(self):
        raise ConfigurationException(FAILED_STATE_MSG)

    @property
    def t(self):
        raise ConfigurationException(FAILED_STATE_MSG)
