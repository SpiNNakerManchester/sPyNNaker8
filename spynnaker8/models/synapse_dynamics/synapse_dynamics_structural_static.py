from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralStatic as StaticStructuralBaseClass
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralCommon as CommonSP


class SynapseDynamicsStructuralStatic(StaticStructuralBaseClass):

    def __init__(
            self, partner_selection, formation, elimination,
            f_rew=CommonSP.DEFAULT_F_REW,
            initial_weight=CommonSP.DEFAULT_INITIAL_WEIGHT,
            initial_delay=CommonSP.DEFAULT_INITIAL_DELAY,
            s_max=CommonSP.DEFAULT_S_MAX, seed=None,
            weight=PyNNStaticSynapse.default_parameters['weight'], delay=None):
        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        StaticStructuralBaseClass.__init__(
            self, partner_selection, formation, elimination, f_rew=f_rew,
            initial_weight=initial_weight, initial_delay=initial_delay,
            s_max=s_max, seed=seed, weight=weight, delay=delay)
