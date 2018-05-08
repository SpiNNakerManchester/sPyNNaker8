from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceCyclic as _BaseClass

_defaults = _BaseClass.default_parameters

class WeightDependenceCyclic(_BaseClass):
    def __init__(self,
        w_min_excit  =1.0, w_max_excit  =2.0, A_plus_excit  =3.0, A_minus_excit  =4.0,
        w_min_excit2 =5.0, w_max_excit2 =6.0, A_plus_excit2 =7.0, A_minus_excit2 =8.0,
        w_min_inhib  =9.0, w_max_inhib  =10.0, A_plus_inhib  =11.0, A_minus_inhib  =12.0,
        w_min_inhib2 =13.0, w_max_inhib2 =14.0, A_plus_inhib2 =15.0, A_minus_inhib2 =16.0):

        super(WeightDependenceMultiplicative, self).__init__(
            w_min_excit = w_min_excit, w_max_excit = w_max_excit,
                A_plus_excit = A_plus_excit, A_minus_excit = A_minus_excit,
            w_min_excit2 = w_min_excit2, w_max_excit2 = w_max_excit2,
                A_plus_excit2 = A_plus_excit2, A_minus_excit2 = A_minus_excit2,
            w_min_inhib = w_min_inhib, w_max_inhib  = w_max_inhib,
                A_plus_inhib  = A_plus_inhib, A_minus_inhib = A_minus_inhib,
            w_min_inhib2 = w_min_inhib2, w_max_inhib2 = w_max_inhib2,
                A_plus_inhib2 = A_plus_inhib2, A_minus_inhib2 = A_minus_inhib2)
