from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralSTDP as STDPStructuralBaseClass
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralCommon as CommonSP
from spinn_front_end_common.utilities import globals_variables


class SynapseDynamicsStructuralSTDP(STDPStructuralBaseClass):

    def __init__(
            self, partner_selection, formation, elimination,
            timing_dependence=None, weight_dependence=None,
            voltage_dependence=None, dendritic_delay_fraction=1.0,
            f_rew=CommonSP.DEFAULT_F_REW,
            initial_weight=CommonSP.DEFAULT_INITIAL_WEIGHT,
            initial_delay=CommonSP.DEFAULT_INITIAL_DELAY,
            s_max=CommonSP.DEFAULT_S_MAX, seed=None,
            weight=PyNNStaticSynapse.default_parameters['weight'], delay=None):

        # move data from timing to weight dependence over as needed to reflect
        # standard structure underneath
        a_plus = timing_dependence.A_plus
        a_minus = timing_dependence.A_minus
        weight_dependence.set_a_plus_a_minus(a_plus=a_plus, a_minus=a_minus)

        if delay is None:
            delay = globals_variables.get_simulator().min_delay

        STDPStructuralBaseClass.__init__(
            self, partner_selection, formation, elimination,
            timing_dependence=timing_dependence,
            weight_dependence=weight_dependence,
            voltage_dependence=voltage_dependence,
            dendritic_delay_fraction=dendritic_delay_fraction, f_rew=f_rew,
            initial_weight=initial_weight, initial_delay=initial_delay,
            s_max=s_max, seed=seed, weight=weight, delay=delay)
