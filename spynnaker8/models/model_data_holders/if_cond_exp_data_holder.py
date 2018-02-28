from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCondExpBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCondExpDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCondExpBase.initialize_parameters['v_init'],
            tau_m=IFCondExpBase.default_parameters['tau_m'],
            cm=IFCondExpBase.default_parameters['cm'],
            v_rest=IFCondExpBase.default_parameters['v_rest'],
            v_reset=IFCondExpBase.default_parameters['v_reset'],
            v_thresh=IFCondExpBase.default_parameters['v_thresh'],
            tau_syn_E=IFCondExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IFCondExpBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCondExpBase.default_parameters['tau_refrac'],
            i_offset=IFCondExpBase.default_parameters['i_offset'],
            e_rev_E=IFCondExpBase.default_parameters['e_rev_E'],
            e_rev_I=IFCondExpBase.default_parameters['e_rev_I'],
            isyn_exc=IFCondExpBase.default_parameters['isyn_exc'],
            isyn_inh=IFCondExpBase.default_parameters['isyn_inh']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCondExpDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label,
            'v_init': v_init, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac, 'i_offset': i_offset,
            'e_rev_E': e_rev_E, 'e_rev_I': e_rev_I, 'isyn_exc': isyn_exc,
            'isyn_inh': isyn_inh})

    @staticmethod
    def build_model():
        return IFCondExpBase
