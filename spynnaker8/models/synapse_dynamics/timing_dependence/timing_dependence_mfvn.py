import logging

from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceMFVN as _BaseClass

logger = logging.getLogger(__name__)


class TimingDependenceMFVN(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus",
        "_beta",
        ]

    def __init__(
            self, tau_plus=20.0, tau_minus=20.0, A_plus=0.01, A_minus=0.01,
            beta=10, sigma=200, alpha=1.0):
        super(TimingDependenceMFVN, self).__init__(
            tau_plus=tau_plus, tau_minus=tau_minus, beta=beta, sigma=sigma,
            kernel_scaling=alpha)
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

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, new_value):
        self._beta = new_value

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, new_value):
        self._sigma = new_value


