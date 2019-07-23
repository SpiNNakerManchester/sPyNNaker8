from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence import (
    WeightDependenceAdditive as
    _BaseClass)


class WeightDependenceAdditive(_BaseClass):
    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0):
        super(WeightDependenceAdditive, self).__init__(
            w_min=w_min, w_max=w_max)
