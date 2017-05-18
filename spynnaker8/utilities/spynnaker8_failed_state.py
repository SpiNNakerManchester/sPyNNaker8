from spinn_front_end_common.utilities import exceptions
from spynnaker.pyNN.utilities.spynnaker_failed_state import SpynnakerFailedState
from spynnaker8.spynnaker8_simulator_interface \
    import Spynnaker8SimulatorInterface


class Spynnaker8FailedState(Spynnaker8SimulatorInterface,
                            SpynnakerFailedState):

    __slots__ = ()
