from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase
from spinn_utilities.abstract_base import abstractproperty
from spinn_utilities.abstract_base import abstractmethod

from spynnaker.pyNN.spynnaker_simulator_interface \
    import SpynnakerSimulatorInterface


@add_metaclass(AbstractBase)
class Spynnaker8SimulatorInterface(SpynnakerSimulatorInterface):

    __slots__ = ()

    @abstractproperty
    def dt(self):
        pass

    # spynnaker_simulator_interface
    # max_delay

    # spynnaker_simulator_interface
    # min_delay

    @abstractproperty
    def mpi_rank(self):
        pass

    @abstractproperty
    def num_processes(self):
        pass

    @abstractproperty
    def recorders(self):
        pass

    # spynnaker_simulator_interface
    # reset()

    # spynnaker_simulator_interface
    # run_until(next)

    @abstractproperty
    def t(self):
        pass


