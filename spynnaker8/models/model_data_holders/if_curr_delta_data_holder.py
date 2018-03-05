from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrDelta

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IfCurrDeltaDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],


            tau_m=IFCurrDelta.default_parameters['tau_m'],
            cm=IFCurrDelta.default_parameters['cm'],
            v_rest=IFCurrDelta.default_parameters['v_rest'],
            v_reset=IFCurrDelta.default_parameters['v_reset'],
            v_thresh=IFCurrDelta.default_parameters['v_thresh'],
            tau_refrac=IFCurrDelta.default_parameters['tau_refrac'],
            i_offset=IFCurrDelta.default_parameters['i_offset'],
            v_init=IFCurrDelta.initialize_parameters['v_init'],
            isyn_exc=IFCurrDelta.default_parameters['isyn_exc'],
            isyn_inh=IFCurrDelta.default_parameters['isyn_inh']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IfCurrDeltaDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label,
            'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_refrac': tau_refrac, 'i_offset': i_offset,
            'v_init': v_init, 'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh})

    @staticmethod
    def build_model():
        return IFCurrDelta
