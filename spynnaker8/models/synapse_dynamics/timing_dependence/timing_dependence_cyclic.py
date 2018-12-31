from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceCyclic as _BaseClass

_defaults = _BaseClass.default_parameters


class TimingDependenceCyclic(_BaseClass):
    __slots__ = [
        "_a_plus",
        "_a_minus"]

    def __init__(
            self,
#             accumulator_depression=_defaults['accumulator_depression'],
#             accumulator_potentiation=_defaults['accumulator_potentiation'],
#             mean_pre_window=_defaults['mean_pre_window'],
#             mean_post_window=_defaults['mean_post_window'],
            accum_decay=_defaults['accum_decay'],
            accum_dep_thresh_excit=_defaults['accum_dep_thresh_excit'],
            accum_pot_thresh_excit=_defaults['accum_pot_thresh_excit'],
            pre_window_tc_excit=_defaults['pre_window_tc_excit'],
            post_window_tc_excit=_defaults['post_window_tc_excit'],
            accum_dep_thresh_excit2=_defaults['accum_dep_thresh_excit2'],
            accum_pot_thresh_excit2=_defaults['accum_pot_thresh_excit2'],
            pre_window_tc_excit2=_defaults['pre_window_tc_excit2'],
            post_window_tc_excit2=_defaults['post_window_tc_excit2'],
            accum_dep_thresh_inhib=_defaults['accum_dep_thresh_inhib'],
            accum_pot_thresh_inhib=_defaults['accum_pot_thresh_inhib'],
            pre_window_tc_inhib=_defaults['pre_window_tc_inhib'],
            post_window_tc_inhib=_defaults['post_window_tc_inhib'],
            accum_dep_thresh_inhib2=_defaults['accum_dep_thresh_inhib2'],
            accum_pot_thresh_inhib2=_defaults['accum_pot_thresh_inhib2'],
            pre_window_tc_inhib2=_defaults['pre_window_tc_inhib2'],
            post_window_tc_inhib2=_defaults['post_window_tc_inhib2'],
            seed=_defaults['seed'],
            random_enabled=_defaults['random_enabled'],
            A_plus=0.01, A_minus=0.01):

        # pylint: disable=too-many-arguments
        super(TimingDependenceCyclic, self).__init__(
            accum_decay=accum_decay,
            accum_dep_thresh_excit=accum_dep_thresh_excit,
            accum_pot_thresh_excit=accum_pot_thresh_excit,
            pre_window_tc_excit=pre_window_tc_excit,
            post_window_tc_excit=post_window_tc_excit,
            accum_dep_thresh_excit2=accum_dep_thresh_excit2,
            accum_pot_thresh_excit2=accum_pot_thresh_excit2,
            pre_window_tc_excit2=pre_window_tc_excit2,
            post_window_tc_excit2=post_window_tc_excit2,
            accum_dep_thresh_inhib=accum_dep_thresh_inhib,
            accum_pot_thresh_inhib=accum_pot_thresh_inhib,
            pre_window_tc_inhib=pre_window_tc_inhib,
            post_window_tc_inhib=post_window_tc_inhib,
            accum_dep_thresh_inhib2=accum_dep_thresh_inhib2,
            accum_pot_thresh_inhib2=accum_pot_thresh_inhib2,
            pre_window_tc_inhib2=pre_window_tc_inhib2,
            post_window_tc_inhib2=post_window_tc_inhib2,
            random_enabled=random_enabled,
            seed=None)
#             accumulator_depression=accumulator_depression,
#             accumulator_potentiation=accumulator_potentiation,
#             mean_pre_window=mean_pre_window,
#             mean_post_window=mean_post_window,
#             dual_fsm=dual_fsm)
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
