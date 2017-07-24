from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceRecurrent as CommonTimingDependenceRecurrent


class TimingDependenceRecurrent(CommonTimingDependenceRecurrent):

    def __init__(
            self, accumulator_depression=CommonTimingDependenceRecurrent.
            default_parameters['accumulator_depression'],
            accumulator_potentiation=CommonTimingDependenceRecurrent.
            default_parameters['accumulator_potentiation'],
            mean_pre_window=CommonTimingDependenceRecurrent.
            default_parameters['mean_pre_window'],
            mean_post_window=CommonTimingDependenceRecurrent.
            default_parameters['mean_post_window'],
            dual_fsm=CommonTimingDependenceRecurrent.
            default_parameters['dual_fsm'], A_plus=0.01, A_minus=0.01):

        CommonTimingDependenceRecurrent.__init__(
            self, accumulator_depression=accumulator_depression,
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
