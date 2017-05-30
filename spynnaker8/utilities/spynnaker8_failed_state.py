from spinn_front_end_common.utilities import exceptions
from spinn_front_end_common.utilities.failed_state import FailedState, \
    FAILED_STATE_MSG
from spynnaker.pyNN.utilities.spynnaker_failed_state \
    import SpynnakerFailedState
from spynnaker8.spynnaker8_simulator_interface \
    import Spynnaker8SimulatorInterface


class Spynnaker8FailedState(Spynnaker8SimulatorInterface,
                            SpynnakerFailedState, object):

    __slots__ = ()

    @property
    def dt(self):
        raise exceptions.ConfigurationException(FAILED_STATE_MSG)

    @property
    def mpi_rank(self):
        pass

    @property
    def num_processes(self):
        pass

    @property
    def recorders(self):
        pass

    @property
    def t(self):
        pass
