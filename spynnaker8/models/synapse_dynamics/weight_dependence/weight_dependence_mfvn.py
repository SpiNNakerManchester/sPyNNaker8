from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceMFVN as _BaseClass


class WeightDependenceMFVN(_BaseClass):
    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0):
        super(WeightDependenceMFVN, self).__init__(
            w_min=w_min, w_max=w_max)
