from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependencePFPC as _BaseClass


class WeightDependencePFPC(_BaseClass):
    __slots__ = [
        "pot_alpha"
        ]

    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0, pot_alpha=0.01):
        super(WeightDependencePFPC, self).__init__(
            w_min=w_min, w_max=w_max, pot_alpha=pot_alpha)

    @property
    def pot_alpha(self):
        return self._pot_alpha

    @pot_alpha.setter
    def pot_alpha(self, new_value):
        self._pot_alpha = new_value
