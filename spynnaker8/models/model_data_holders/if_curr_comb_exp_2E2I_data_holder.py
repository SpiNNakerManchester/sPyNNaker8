from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrCombExp2E2I

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCurrCombExp2E2IDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCurrCombExp2E2I.initialize_parameters['v_init'],
            tau_m=IFCurrCombExp2E2I.default_parameters['tau_m'],
            cm=IFCurrCombExp2E2I.default_parameters['cm'],
            v_rest=IFCurrCombExp2E2I.default_parameters['v_rest'],
            v_reset=IFCurrCombExp2E2I.default_parameters['v_reset'],
            v_thresh=IFCurrCombExp2E2I.default_parameters['v_thresh'],
            tau_refrac=IFCurrCombExp2E2I.default_parameters['tau_refrac'],
            i_offset=IFCurrCombExp2E2I.default_parameters['i_offset'],

            # excitatory
            exc_a_response=IFCurrCombExp2E2I.default_parameters['exc_a_response'],
            exc_a_A=IFCurrCombExp2E2I.default_parameters['exc_a_A'],
            exc_a_tau=IFCurrCombExp2E2I.default_parameters['exc_a_tau'],
            exc_b_response=IFCurrCombExp2E2I.default_parameters['exc_b_response'],
            exc_b_B=IFCurrCombExp2E2I.default_parameters['exc_b_B'],
            exc_b_tau=IFCurrCombExp2E2I.default_parameters['exc_b_tau'],

            # excitatory2
            exc2_a_response=IFCurrCombExp2E2I.default_parameters['exc2_a_response'],
            exc2_a_A=IFCurrCombExp2E2I.default_parameters['exc2_a_A'],
            exc2_a_tau=IFCurrCombExp2E2I.default_parameters['exc2_a_tau'],
            exc2_b_response=IFCurrCombExp2E2I.default_parameters['exc2_b_response'],
            exc2_b_B=IFCurrCombExp2E2I.default_parameters['exc2_b_B'],
            exc2_b_tau=IFCurrCombExp2E2I.default_parameters['exc2_b_tau'],

            # inhibitory
            inh_a_response=IFCurrCombExp2E2I.default_parameters['inh_a_response'],
            inh_a_A=IFCurrCombExp2E2I.default_parameters['inh_a_A'],
            inh_a_tau=IFCurrCombExp2E2I.default_parameters['inh_a_tau'],
            inh_b_response=IFCurrCombExp2E2I.default_parameters['inh_b_response'],
            inh_b_B=IFCurrCombExp2E2I.default_parameters['inh_b_B'],
            inh_b_tau=IFCurrCombExp2E2I.default_parameters['inh_b_tau'],

            # inhibitory2
            inh2_a_response=IFCurrCombExp2E2I.default_parameters['inh2_a_response'],
            inh2_a_A=IFCurrCombExp2E2I.default_parameters['inh2_a_A'],
            inh2_a_tau=IFCurrCombExp2E2I.default_parameters['inh2_a_tau'],
            inh2_b_response=IFCurrCombExp2E2I.default_parameters['inh2_b_response'],
            inh2_b_B=IFCurrCombExp2E2I.default_parameters['inh2_b_B'],
            inh2_b_tau=IFCurrCombExp2E2I.default_parameters['inh2_b_tau']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCurrCombExp2E2IDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_refrac': tau_refrac, 'i_offset': i_offset,
            'v_init': v_init,
            # excitatory
            'exc_a_response': exc_a_response,
            'exc_a_A': exc_a_A,
            'exc_a_tau': exc_a_tau,
            'exc_b_response': exc_b_response,
            'exc_b_B': exc_b_B,
            'exc_b_tau': exc_b_tau,
            # excitatory 2
            'exc2_a_response': exc2_a_response,
            'exc2_a_A': exc2_a_A,
            'exc2_a_tau': exc2_a_tau,
            'exc2_b_response': exc2_b_response,
            'exc2_b_B': exc2_b_B,
            'exc2_b_tau': exc2_b_tau,
            # inhibitory
            'inh_a_response': inh_a_response,
            'inh_a_A': inh_a_A,
            'inh_a_tau': inh_a_tau,
            'inh_b_response': inh_b_response,
            'inh_b_B': inh_b_B,
            'inh_b_tau': inh_b_tau,
            # inhibitory 2
            'inh2_a_response': inh2_a_response,
            'inh2_a_A': inh2_a_A,
            'inh2_a_tau': inh2_a_tau,
            'inh2_b_response': inh2_b_response,
            'inh2_b_B': inh2_b_B,
            'inh2_b_tau': inh2_b_tau,
            })

    @staticmethod
    def build_model():
        return IFCurrCombExp2E2I
