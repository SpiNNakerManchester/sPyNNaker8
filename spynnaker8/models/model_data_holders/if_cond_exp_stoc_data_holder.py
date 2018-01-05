from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCondExpStoc

_apv_defaults = AbstractPopulationVertex.none_pynn_default_parameters


class IfCondExpStocDataHolder(DataHolder):

    def __init__(
            self,

            spikes_per_second=_apv_defaults['spikes_per_second'],
            ring_buffer_sigma=_apv_defaults['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defaults[
                'incoming_spike_buffer_size'],
            constraints=_apv_defaults['constraints'],
            label=_apv_defaults['label'],

            v_init=IFCondExpStoc.none_pynn_default_parameters['v_init'],

            tau_m=IFCondExpStoc.default_parameters['tau_m'],
            cm=IFCondExpStoc.default_parameters['cm'],
            v_rest=IFCondExpStoc.default_parameters['v_rest'],
            v_reset=IFCondExpStoc.default_parameters['v_reset'],
            v_thresh=IFCondExpStoc.default_parameters['v_thresh'],
            tau_syn_E=IFCondExpStoc.default_parameters['tau_syn_E'],
            tau_syn_I=IFCondExpStoc.default_parameters['tau_syn_I'],
            tau_refrac=IFCondExpStoc.default_parameters['tau_refrac'],
            i_offset=IFCondExpStoc.default_parameters['i_offset'],
            e_rev_E=IFCondExpStoc.default_parameters['e_rev_E'],
            e_rev_I=IFCondExpStoc.default_parameters['e_rev_I'],
            du_th=IFCondExpStoc.default_parameters['du_th'],
            tau_th=IFCondExpStoc.default_parameters['tau_th'],
            isyn_exc=IFCondExpStoc.default_parameters['isyn_exc'],
            isyn_inh=IFCondExpStoc.default_parameters['isyn_inh']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IfCondExpStocDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label,
            'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac, 'i_offset': i_offset,
            'e_rev_E': e_rev_E, 'e_rev_I': e_rev_I, 'du_th': du_th,
            'tau_th': tau_th, 'v_init': v_init, 'isyn_exc': isyn_exc,
            'isyn_inh': isyn_inh})

    @staticmethod
    def build_model():
        return IFCondExpStoc
