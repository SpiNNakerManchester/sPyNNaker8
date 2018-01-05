from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceSpikeNearestPair as \
    CommonTimingDependanceSpikeNearestPair

_defaults = CommonTimingDependanceSpikeNearestPair.default_parameters


class TimingDependenceSpikeNearestPair(
        CommonTimingDependanceSpikeNearestPair):

    def __init__(
            self, tau_plus=_defaults['tau_plus'],
            tau_minus=_defaults['tau_minus'],
            A_plus=0.01, A_minus=0.01):
        super(TimingDependenceSpikeNearestPair, self).__init__(
            tau_plus=tau_plus, tau_minus=tau_minus)

        self._a_plus = A_plus
        self._a_minus = A_minus

    @property
    def A_plus(self):
        return self._a_plus

    @A_plus.setter
    def A_plus(self, new_value):
        self._a_plus = new_value

    @property
    def A_minus(self):
        return self._a_minus

    @A_minus.setter
    def A_minus(self, new_value):
        self._a_minus = new_value
