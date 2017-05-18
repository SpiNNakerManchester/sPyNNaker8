from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase
from spinn_utilities.abstract_base import abstractproperty
from spinn_utilities.abstract_base import abstractmethod

from spynnaker.pyNN.spynnaker_simulator_interface \
    import SpynnakerSimulatorInterface


@add_metaclass(AbstractBase)
class Spynnaker8SimulatorInterface(SpynnakerSimulatorInterface):

    __slots__ = ()

