from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrExpGrazAdaptive

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCurrExpGrazAdaptiveDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrExpGrazAdaptive.initialize_parameters['v_init'],
            tau_m=IFCurrExpGrazAdaptive.default_parameters['tau_m'],
            cm=IFCurrExpGrazAdaptive.default_parameters['cm'],
            v_rest=IFCurrExpGrazAdaptive.default_parameters['v_rest'],
            v_reset=IFCurrExpGrazAdaptive.default_parameters['v_reset'],

            # Adaptive threshold parameters
            thresh_B=IFCurrExpGrazAdaptive.default_parameters['thresh_B'],
            thresh_b=IFCurrExpGrazAdaptive.default_parameters['thresh_b'],
            thresh_b_0=IFCurrExpGrazAdaptive.default_parameters['thresh_b_0'],
            thresh_tau_a=IFCurrExpGrazAdaptive.default_parameters['thresh_tau_a'],
            thresh_beta=IFCurrExpGrazAdaptive.default_parameters['thresh_beta'],

            tau_syn_E=IFCurrExpGrazAdaptive.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrExpGrazAdaptive.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrExpGrazAdaptive.default_parameters['tau_refrac'],
            i_offset=IFCurrExpGrazAdaptive.default_parameters['i_offset']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrExpGrazAdaptiveDataHolder, self).__init__({
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

            'tau_syn_E': tau_syn_E,
            'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac,
            'i_offset': i_offset,
            'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrExpGrazAdaptive
