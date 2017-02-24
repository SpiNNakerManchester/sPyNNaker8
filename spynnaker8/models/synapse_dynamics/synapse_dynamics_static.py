from spynnaker.pyNN.models.neuron.synapse_dynamics.synapse_dynamics_static \
    import SynapseDynamicsStatic as CommonSynapseDynamicsStatic
from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse


class SynapseDynamicsStatic(CommonSynapseDynamicsStatic):
    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=PyNNStaticSynapse.default_parameters['delay']):

        CommonSynapseDynamicsStatic.__init__(self)
        self._weight = weight
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
