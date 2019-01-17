from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence\
    import TimingDependenceVogels2011 as _BaseClass

_defaults = _BaseClass.default_parameters


class TimingDependenceVogels2011(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus"]

    def __init__(
            self, alpha, tau=_defaults['tau'], A_plus=0.01, A_minus=0.01):
        super(TimingDependenceVogels2011, self).__init__(tau=tau, alpha=alpha)
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
