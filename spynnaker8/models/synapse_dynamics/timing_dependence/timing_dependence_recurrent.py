from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence import (
    TimingDependenceRecurrent as
    _BaseClass)

_defaults = _BaseClass.default_parameters


class TimingDependenceRecurrent(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus"]

    def __init__(
            self, accumulator_depression=_defaults['accumulator_depression'],
            accumulator_potentiation=_defaults['accumulator_potentiation'],
            mean_pre_window=_defaults['mean_pre_window'],
            mean_post_window=_defaults['mean_post_window'],
            dual_fsm=_defaults['dual_fsm'], A_plus=0.01, A_minus=0.01):
        # pylint: disable=too-many-arguments
        super(TimingDependenceRecurrent, self).__init__(
            accumulator_depression=accumulator_depression,
            accumulator_potentiation=accumulator_potentiation,
            mean_pre_window=mean_pre_window,
            mean_post_window=mean_post_window,
            dual_fsm=dual_fsm)
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
