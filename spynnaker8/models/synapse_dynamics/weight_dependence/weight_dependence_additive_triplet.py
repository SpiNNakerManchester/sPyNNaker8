from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence import (
    WeightDependenceAdditiveTriplet as
    _BaseClass)


class WeightDependenceAdditiveTriplet(_BaseClass):

    # noinspection PyPep8Naming
    def __init__(
            self, w_min=0.0, w_max=1.0, A3_plus=0.01, A3_minus=0.01):
        super(WeightDependenceAdditiveTriplet, self).__init__(
            w_max=w_max, w_min=w_min, A3_plus=A3_plus, A3_minus=A3_minus)
