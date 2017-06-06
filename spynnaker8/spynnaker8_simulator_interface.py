from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase
from spinn_utilities.abstract_base import abstractproperty

from spynnaker.pyNN.spynnaker_simulator_interface \
    import SpynnakerSimulatorInterface


@add_metaclass(AbstractBase)
class Spynnaker8SimulatorInterface(SpynnakerSimulatorInterface):

    __slots__ = ()

    @abstractproperty
    def dt(self):
        pass

    @abstractproperty
    def mpi_rank(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def num_processes(self):
        pass

    @abstractproperty
    def recorders(self):
        pass

    @abstractproperty
    def segment_counter(self):
        pass

    @abstractproperty
    def t(self):
        pass
