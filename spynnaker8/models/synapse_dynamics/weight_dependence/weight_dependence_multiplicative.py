from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceMultiplicative as _BaseClass


class WeightDependenceMultiplicative(_BaseClass):
    def __init__(self, w_min=0.0, w_max=1.0):
        super(WeightDependenceMultiplicative, self).__init__(
            w_max=w_max, w_min=w_min)
