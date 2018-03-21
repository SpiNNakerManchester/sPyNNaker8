from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralStatic as StaticStructuralBaseClass
from spynnaker.pyNN.models.neuron.synapse_dynamics \
    import SynapseDynamicsStructuralCommon as StructuralBaseClass
from spinn_front_end_common.utilities import globals_variables
from spynnaker8.models.synapse_dynamics import SynapseDynamicsStatic


class SynapseDynamicsStructuralStatic(StaticStructuralBaseClass):
    """ Class enables synaptic rewiring. It acts as a wrapper around \
        SynapseDynamicsStatic or SynapseDynamicsSTDP. This means rewiring \
        can operate in parallel with these types of synapses.

        Written by Petrut Bogdan.


        Example usage to allow rewiring in parallel with STDP::

            stdp_model = sim.STDPMechanism(...)

            structure_model_with_stdp = sim.StructuralMechanismStatic(
                stdp_model=stdp_model,
                weight=0,
                s_max=32,
                grid=[np.sqrt(pop_size), np.sqrt(pop_size)],
                random_partner=True,
                f_rew=10 ** 4,  # Hz
                sigma_form_forward=1.,
                delay=10
            )
            plastic_projection = sim.Projection(
                ...,
                synapse_type=structure_model_with_stdp
            )


    :param f_rew: Frequency of rewiring (Hz). How many rewiring attempts will
        be done per second.
    :type f_rew: int
    :param weight: Initial weight assigned to a newly formed connection
    :type weight: float
    :param delay: Delay assigned to a newly formed connection
    :type delay: int
    :param s_max: Maximum fan-in per target layer neuron
    :type s_max: int
    :param sigma_form_forward: Spread of feed-forward formation receptive field
    :type sigma_form_forward: float
    :param sigma_form_lateral: Spread of lateral formation receptive field
    :type sigma_form_lateral: float
    :param p_form_forward: Peak probability for feed-forward formation
    :type p_form_forward: float
    :param p_form_lateral: Peak probability for lateral formation
    :type p_form_lateral: float
    :param p_elim_pot: Probability of elimination of a potentiated synapse
    :type p_elim_pot: float
    :param p_elim_dep: Probability of elimination of a depressed synapse
    :type p_elim_dep: float
    :param grid: Grid shape
    :type grid: 2d int array
    :param lateral_inhibition: Flag whether to mark synapses formed within a
        layer as inhibitory or excitatory
    :type lateral_inhibition: bool
    :param random_partner: Flag whether to randomly select pre-synaptic
        partner for formation
    :type random_partner: bool
    :param seed: seed the random number generators
    :type seed: int
    """
    __slots__ = [
        "_weight",
        "_delay"]

    def __init__(
            self,
            stdp_model=StructuralBaseClass.default_parameters['stdp_model'],
            f_rew=StructuralBaseClass.default_parameters['f_rew'],
            weight=StructuralBaseClass.default_parameters['weight'],
            delay=StructuralBaseClass.default_parameters['delay'],
            s_max=StructuralBaseClass.default_parameters['s_max'],
            sigma_form_forward=StructuralBaseClass.default_parameters[
                'sigma_form_forward'],
            sigma_form_lateral=StructuralBaseClass.default_parameters[
                'sigma_form_lateral'],
            p_form_forward=StructuralBaseClass.default_parameters[
                'p_form_forward'],
            p_form_lateral=StructuralBaseClass.default_parameters[
                'p_form_lateral'],
            p_elim_dep=StructuralBaseClass.default_parameters['p_elim_dep'],
            p_elim_pot=StructuralBaseClass.default_parameters['p_elim_pot'],
            grid=StructuralBaseClass.default_parameters['grid'],
            lateral_inhibition=StructuralBaseClass.default_parameters[
                'lateral_inhibition'],
            random_partner=StructuralBaseClass.default_parameters[
                'random_partner'],
            seed=None):

        if not stdp_model:
            stdp_model = SynapseDynamicsStatic()

        super(SynapseDynamicsStructuralStatic, self).__init__(
            stdp_model=stdp_model, f_rew=f_rew, weight=weight, delay=delay,
            s_max=s_max, sigma_form_forward=sigma_form_forward,
            sigma_form_lateral=sigma_form_lateral,
            p_form_forward=p_form_forward, p_form_lateral=p_form_lateral,
            p_elim_dep=p_elim_dep, p_elim_pot=p_elim_pot,
            grid=grid, lateral_inhibition=lateral_inhibition,
            random_partner=random_partner, seed=seed
        )

        self._weight = stdp_model._weight
        _delay = stdp_model.delay
        if _delay is None:
            _delay = globals_variables.get_simulator().min_delay
        self._delay = _delay

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_value):
        self._weight = new_value

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, new_value):
        self._delay = new_value
