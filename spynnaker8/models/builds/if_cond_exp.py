from pyNN.standardmodels.cells import IF_cond_exp as PyNNIfCondExp
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_base import IFCondExpBase
from spynnaker.pyNN.utilities import globals_variables
from spynnaker8.models.builds.build_common import BuildCommon


class IFCondExp(IFCondExpBase, PyNNIfCondExp, BuildCommon):
    """ Leaky integrate and fire neuron with an exponentially decaying \
        conductance input
    """

    def __init__(
            self, size, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            tau_m=PyNNIfCondExp.default_parameters['tau_m'],
            cm=PyNNIfCondExp.default_parameters['cm'],
            v_rest=PyNNIfCondExp.default_parameters['v_rest'],
            v_reset=PyNNIfCondExp.default_parameters['v_reset'],
            v_thresh=PyNNIfCondExp.default_parameters['v_thresh'],
            tau_syn_E=PyNNIfCondExp.default_parameters['tau_syn_E'],
            tau_syn_I=PyNNIfCondExp.default_parameters['tau_syn_I'],
            tau_refrac=PyNNIfCondExp.default_parameters['tau_refrac'],
            i_offset=PyNNIfCondExp.default_parameters['i_offset'],
            e_rev_E=PyNNIfCondExp.default_parameters['e_rev_E'],
            e_rev_I=PyNNIfCondExp.default_parameters['e_rev_I'], v_init=None):
        IFCondExpBase.__init__(
            self, n_neurons=size, spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma, constraints=constraints,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            label=label, tau_m=tau_m, cm=cm, v_init=v_init, v_reset=v_reset,
            v_rest=v_rest, v_thresh=v_thresh, tau_refrac=tau_refrac,
            tau_syn_E=tau_syn_E, tau_syn_I=tau_syn_I, i_offset=i_offset,
            e_rev_E=e_rev_E, e_rev_I=e_rev_I,
            config=globals_variables.get_simulator().config)
        PyNNIfCondExp.__init__(self)
        BuildCommon.__init__(self, self)
