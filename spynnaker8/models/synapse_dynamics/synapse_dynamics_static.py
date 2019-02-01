from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStatic as _BaseClass
from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables


class SynapseDynamicsStatic(_BaseClass):
    __slots__ = [
        "__delay",
        "__weight"]

    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=None):
        super(SynapseDynamicsStatic, self).__init__()
        self.__weight = weight

        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        self.__delay = delay

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, new_value):
        self.__weight = new_value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, new_value):
        self.__delay = new_value
