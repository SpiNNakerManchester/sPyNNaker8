from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrAlpha

_apv_defs = AbstractPopulationVertex.none_pynn_default_parameters


class IFCurrAlphaDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrAlpha.non_pynn_default_parameters['v_init'],

            tau_m=IFCurrAlpha.default_parameters['tau_m'],
            cm=IFCurrAlpha.default_parameters['cm'],
            v_rest=IFCurrAlpha.default_parameters['v_rest'],
            v_reset=IFCurrAlpha.default_parameters['v_reset'],
            v_thresh=IFCurrAlpha.default_parameters['v_thresh'],
            tau_syn_E=IFCurrAlpha.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrAlpha.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrAlpha.default_parameters['tau_refrac'],
            i_offset=IFCurrAlpha.default_parameters['i_offset']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrAlphaDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac, 'i_offset': i_offset,
            'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrAlpha
