from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence\
    import TimingDependenceVogels2011 as CommonTimingDependenceVogels2011


class TimingDependenceVogels2011(CommonTimingDependenceVogels2011):

    def __init__(
            self, alpha,
            tau=CommonTimingDependenceVogels2011.default_parameters['tau'],
            A_plus=0.01, A_minus=0.01):
        CommonTimingDependenceVogels2011.__init__(self, tau=tau, alpha=alpha)
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
