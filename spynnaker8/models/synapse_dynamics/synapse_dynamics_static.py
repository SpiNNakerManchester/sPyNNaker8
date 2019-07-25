from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.models.neuron.synapse_dynamics import (
    SynapseDynamicsStatic as _BaseClass)


class SynapseDynamicsStatic(_BaseClass):

    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=None):
        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        super(SynapseDynamicsStatic, self).__init__(weight, delay)
