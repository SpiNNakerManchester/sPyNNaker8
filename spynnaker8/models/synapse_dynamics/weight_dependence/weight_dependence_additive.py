from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence\
    .common_weight_dependence_additive import CommonWeightDependenceAdditive


class WeightDependenceAdditive(CommonWeightDependenceAdditive):

    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0):
        CommonWeightDependenceAdditive.__init__(
            self, w_min=w_min, w_max=w_max)
