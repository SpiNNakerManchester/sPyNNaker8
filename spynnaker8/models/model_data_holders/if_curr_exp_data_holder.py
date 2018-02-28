from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrExpBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCurrExpDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrExpBase.initialize_parameters['v_init'],
            tau_m=IFCurrExpBase.default_parameters['tau_m'],
            cm=IFCurrExpBase.default_parameters['cm'],
            v_rest=IFCurrExpBase.default_parameters['v_rest'],
            v_reset=IFCurrExpBase.default_parameters['v_reset'],
            v_thresh=IFCurrExpBase.default_parameters['v_thresh'],
            tau_syn_E=IFCurrExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrExpBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrExpBase.default_parameters['tau_refrac'],
            i_offset=IFCurrExpBase.default_parameters['i_offset']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrExpDataHolder, self).__init__({
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
        return IFCurrExpBase
