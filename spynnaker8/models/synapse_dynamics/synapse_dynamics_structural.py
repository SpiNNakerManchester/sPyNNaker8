from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructural as _BaseClass
from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
import numpy as np

from spynnaker8.models.synapse_dynamics import SynapseDynamicsSTDP, \
    SynapseDynamicsStatic


class SynapseDynamicsStructural(_BaseClass):
    __slots__ = [
        "_f_rew",
        "_p_rew",
        "_weight",
        "_delay",
        "_s_max",
        "_lateral_inhibition",
        "_sigma_form_forward",
        "_sigma_form_lateral",
        "_p_form_forward",
        "_p_form_lateral",
        "_p_elim_dep",
        "_p_elim_pot",
        "_grid",
        "_random_partner",
        "_connections",
        "_actual_row_max_length"]

    def __init__(self, stdp_model=None, f_rew=10 ** 4, weight=0, delay=1,
                 s_max=32, sigma_form_forward=2.5, sigma_form_lateral=1,
                 p_form_forward=0.16, p_form_lateral=1,
                 p_elim_dep=0.0245, p_elim_pot=1.36 * 10 ** -4,
                 grid=np.array([16, 16]), lateral_inhibition=0,
                 random_partner=False,
                 seed=None):
        # if stdp_model and isinstance(stdp_model, SynapseDynamicsSTDP):
        if not stdp_model:
            stdp_model = SynapseDynamicsStatic()

        super(SynapseDynamicsStructural, self).__init__(
            stdp_model=stdp_model, f_rew=f_rew, weight=weight, delay=delay,
            s_max=s_max, sigma_form_forward=sigma_form_forward,
            sigma_form_lateral=sigma_form_lateral,
            p_form_forward=p_form_forward, p_form_lateral=p_form_lateral,
            p_elim_dep=p_elim_dep, p_elim_pot=p_elim_pot,
            grid=grid, lateral_inhibition=lateral_inhibition,
            random_partner=random_partner, seed=seed
        )

        self._weights = stdp_model._weight
        _delays = stdp_model.delay
        if _delays is None:
            _delays = globals_variables.get_simulator().min_delay
        self._delays = _delays

    @property
    def weight(self):
        return self._weights

    @weight.setter
    def weight(self, new_value):
        self._weights = new_value

    @property
    def delay(self):
        return self._delays

    @delay.setter
    def delay(self, new_value):
        self._delays = new_value
