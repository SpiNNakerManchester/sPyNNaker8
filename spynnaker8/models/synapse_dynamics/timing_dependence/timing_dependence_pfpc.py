import logging

from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependencePFPC as _BaseClass

logger = logging.getLogger(__name__)


class TimingDependencePFPC(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus",
        "_t_peak"
        ]

    def __init__(
            self, tau_plus=20.0, tau_minus=20.0, A_plus=0.01, A_minus=0.01,
            t_peak=100, alpha=1.0):
        super(TimingDependencePFPC, self).__init__(
            tau_plus=tau_plus, tau_minus=tau_minus, t_peak=t_peak, kernel_scaling=alpha)
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
    def t_peak(self):
        return self._t_peak

    @t_peak.setter
    def t_peak(self, new_value):
        self._t_peak = new_value
