from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrDualExpBase

_apv_defs = AbstractPopulationVertex.none_pynn_default_parameters


class IFCurrDualExpDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrDualExpBase.none_pynn_default_parameters['v_init'],

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
            isyn_exc=IFCurrDualExpBase.default_parameters['isyn_exc'],
            isyn_inh=IFCurrDualExpBase.default_parameters['isyn_inh'],
            isyn_exc2=IFCurrDualExpBase.default_parameters['isyn_exc2']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrDualExpDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma, 'label': label,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'tau_refrac': tau_refrac,
            'tau_m': tau_m, 'tau_syn_E': tau_syn_E, 'cm': cm,
            'v_rest': v_rest, 'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_syn_E2': tau_syn_E2, 'tau_syn_I': tau_syn_I,
            'i_offset': i_offset, 'v_init': v_init,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
            'isyn_exc2': isyn_exc2})

    @staticmethod
    def build_model():
        return IFCurrDualExpBase
