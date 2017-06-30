from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence.\
    common_weight_dependence_multiplicative import \
    CommonWeightDependenceMultiplicative


class WeightDependenceMultiplicative(CommonWeightDependenceMultiplicative):

    def __init__(self, w_min=0.0, w_max=1.0):
        CommonWeightDependenceMultiplicative.__init__(
            self, w_max=w_max, w_min=w_min)
