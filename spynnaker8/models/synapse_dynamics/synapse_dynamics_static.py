from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.models.neuron.synapse_dynamics import (
    SynapseDynamicsStatic as _BaseClass)


class SynapseDynamicsStatic(_BaseClass):
    __slots__ = [
        "_delay",
        "_weight"]

    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=None):
        super(SynapseDynamicsStatic, self).__init__()
        self._weight = weight

        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        self._delay = delay

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_value):
        self._weight = new_value

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, new_value):
        self._delay = new_value
