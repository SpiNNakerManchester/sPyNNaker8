from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceCyclic as _BaseClass

_defaults = _BaseClass.default_parameters

class WeightDependenceCyclic(_BaseClass):
    def __init__(self,
        w_min_excit = _defaults['w_min_excit'], w_max_excit = _defaults['w_max_excit'],
            A_plus_excit = _defaults['A_plus_excit'], A_minus_excit = _defaults['A_minus_excit'],
        w_min_excit = _defaults['w_min_excit'], w_max_excit = _defaults['w_max_excit'],
            A_plus_excit = _defaults['A_plus_excit'], A_minus_excit = _defaults['A_minus_excit'],
        w_min_inhib = _defaults['w_min_inhib'], w_max_inhib = _defaults['w_max_inhib'],
            A_plus_inhib = _defaults['A_plus_inhib'], A_minus_inhib = _defaults['A_minus_inhib'],
        w_min_inhib2 = _defaults['w_min_inhib2'], w_max_inhib2 = _defaults['w_max_inhib2'],
            A_plus_inhib2 = _defaults['A_plus_inhib2'], A_minus_inhib2 = _defaults['A_minus_inhib2']):

        super(WeightDependenceMultiplicative, self).__init__(
            w_min_excit = w_min_excit, w_max_excit = w_max_excit,
                A_plus_excit = A_plus_excit, A_minus_excit = A_minus_excit,
            w_min_excit2 = w_min_excit2, w_max_excit2 = w_max_excit2,
                A_plus_excit2 = A_plus_excit2, A_minus_excit2 = A_minus_excit2,
            w_min_inhib = w_min_inhib, w_max_inhib = w_max_inhib,
                A_plus_inhib  = A_plus_inhib, A_minus_inhib = A_minus_inhib,
            w_min_inhib2 = w_min_inhib2, w_max_inhib2 = w_max_inhib2,
                A_plus_inhib2 = A_plus_inhib2, A_minus_inhib2 = A_minus_inhib2)
