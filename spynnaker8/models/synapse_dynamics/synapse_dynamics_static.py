from spynnaker.pyNN.models.neuron.synapse_dynamics.synapse_dynamics_static \
    import SynapseDynamicsStatic as CommonSynapseDynamicsStatic
from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse


class SynapseDynamicsStatic(CommonSynapseDynamicsStatic, PyNNStaticSynapse):
    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=PyNNStaticSynapse.default_parameters['delay']):
        CommonSynapseDynamicsStatic.__init__(self)
        PyNNStaticSynapse.__init__(self, weight=weight, delay=delay)
