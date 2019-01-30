from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceERBP as _BaseClass


class WeightDependenceERBP(_BaseClass):
    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0):
        super(WeightDependenceERBP, self).__init__(
            w_min=w_min, w_max=w_max)
