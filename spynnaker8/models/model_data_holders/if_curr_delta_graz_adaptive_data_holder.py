from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrDeltaGrazAdaptive

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCurrDeltaGrazAdaptiveDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrDeltaGrazAdaptive.initialize_parameters['v_init'],
            tau_m=IFCurrDeltaGrazAdaptive.default_parameters['tau_m'],
            cm=IFCurrDeltaGrazAdaptive.default_parameters['cm'],
            v_rest=IFCurrDeltaGrazAdaptive.default_parameters['v_rest'],
            v_reset=IFCurrDeltaGrazAdaptive.default_parameters['v_reset'],

            # Adaptive threshold parameters
            thresh_B=IFCurrDeltaGrazAdaptive.default_parameters['thresh_B'],
            thresh_b=IFCurrDeltaGrazAdaptive.default_parameters['thresh_b'],
            thresh_b_0=IFCurrDeltaGrazAdaptive.default_parameters['thresh_b_0'],
            thresh_tau_a=IFCurrDeltaGrazAdaptive.default_parameters['thresh_tau_a'],
            thresh_beta=IFCurrDeltaGrazAdaptive.default_parameters['thresh_beta'],

#             tau_syn_E=IFCurrDeltaGrazAdaptive.default_parameters['tau_syn_E'],
#             tau_syn_I=IFCurrDeltaGrazAdaptive.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrDeltaGrazAdaptive.default_parameters['tau_refrac'],
            i_offset=IFCurrDeltaGrazAdaptive.default_parameters['i_offset']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrDeltaGrazAdaptiveDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'tau_m': tau_m,
            'cm': cm,
            'v_rest': v_rest,
            'v_reset': v_reset,

            'thresh_B': thresh_B,
            'thresh_b': thresh_b,
            'thresh_b_0': thresh_b_0,
            'thresh_tau_a': thresh_tau_a,
            'thresh_beta': thresh_beta,

#             'tau_syn_E': tau_syn_E,
#             'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac,
            'i_offset': i_offset,
            'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrDeltaGrazAdaptive
