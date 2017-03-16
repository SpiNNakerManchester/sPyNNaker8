from spynnaker.pyNN.models.neuron.synapse_dynamics.synapse_dynamics_static \
    import SynapseDynamicsStatic as CommonSynapseDynamicsStatic
from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spynnaker.pyNN.utilities import globals_variables


class SynapseDynamicsStatic(CommonSynapseDynamicsStatic):
    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=None):

        CommonSynapseDynamicsStatic.__init__(self)
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
