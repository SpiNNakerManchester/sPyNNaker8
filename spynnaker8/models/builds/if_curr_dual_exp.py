from pyNN.standardmodels import StandardCellType as PyNNStandardCellType

from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base import \
    IFCurrDualExpBase

from spynnaker8.models.builds.build_common import BuildCommon


class IFCurrDualExp(IFCurrDualExpBase, PyNNStandardCellType, BuildCommon):
    """ Leaky integrate and fire neuron with two exponentially decaying \
        excitatory current inputs, and one exponentially decaying inhibitory \
        current input
    """

    def __init__(
            self, size, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            tau_m=IFCurrDualExpBase.default_parameters['tau_m'],
            cm=IFCurrDualExpBase.default_parameters['cm'],
            v_rest=IFCurrDualExpBase.default_parameters['v_rest'],
            v_reset=IFCurrDualExpBase.default_parameters['v_reset'],
            v_thresh=IFCurrDualExpBase.default_parameters['v_thresh'],
            tau_syn_E=IFCurrDualExpBase.default_parameters['tau_syn_E'],
            tau_syn_E2=IFCurrDualExpBase.default_parameters['tau_syn_E2'],
            tau_syn_I=IFCurrDualExpBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrDualExpBase.default_parameters['tau_refrac'],
            i_offset=IFCurrDualExpBase.default_parameters['i_offset'],
            v_init=None):
        IFCurrDualExpBase.__init__(
            self, n_neurons=size, spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma, label=label,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            constraints=constraints, tau_refrac=tau_refrac, tau_m=tau_m,
            tau_syn_E=tau_syn_E, cm=cm, v_rest=v_rest, v_reset=v_reset,
            v_thresh=v_thresh, tau_syn_E2=tau_syn_E2, tau_syn_I=tau_syn_I,
            i_offset=i_offset, v_init=v_init)
        PyNNStandardCellType.__init__(self)
        BuildCommon.__init__(self, self)

    @staticmethod
    def set_model_max_atoms_per_core(new_value):
        IFCurrDualExpBase._model_based_max_atoms_per_core = new_value

    @staticmethod
    def get_max_atoms_per_core():
        return IFCurrDualExpBase._model_based_max_atoms_per_core
