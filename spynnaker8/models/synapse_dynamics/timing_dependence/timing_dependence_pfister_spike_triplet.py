from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence import (
    TimingDependencePfisterSpikeTriplet as
    _BaseClass)


class TimingDependencePfisterSpikeTriplet(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus"]

    # noinspection PyPep8Naming
    def __init__(
            self, tau_plus, tau_minus, tau_x, tau_y, A_plus=0.01,
            A_minus=0.01):
        # pylint: disable=too-many-arguments
        super(TimingDependencePfisterSpikeTriplet, self).__init__(
            tau_plus=tau_plus, tau_minus=tau_minus, tau_x=tau_x,
            tau_y=tau_y)

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
