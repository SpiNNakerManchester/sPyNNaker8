from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCondExp2E2I

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IFCondExp2E2IDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            v_init=IFCondExp2E2I.initialize_parameters['v_init'],
            tau_m=IFCondExp2E2I.default_parameters['tau_m'],
            cm=IFCondExp2E2I.default_parameters['cm'],
            v_rest=IFCondExp2E2I.default_parameters['v_rest'],
            v_reset=IFCondExp2E2I.default_parameters['v_reset'],
            v_thresh=IFCondExp2E2I.default_parameters['v_thresh'],
            tau_refrac=IFCondExp2E2I.default_parameters['tau_refrac'],
            i_offset=IFCondExp2E2I.default_parameters['i_offset'],

            tau_syn_E=IFCondExp2E2I.default_parameters['tau_syn_E'],
            tau_syn_E2=IFCondExp2E2I.default_parameters['tau_syn_E2'],
            tau_syn_I=IFCondExp2E2I.default_parameters['tau_syn_I'],
            tau_syn_I2=IFCondExp2E2I.default_parameters['tau_syn_I2'],
            e_rev_E=IFCondExp2E2I.default_parameters['e_rev_E'],
            e_rev_E2=IFCondExp2E2I.default_parameters['e_rev_E2'],
            e_rev_I=IFCondExp2E2I.default_parameters['e_rev_I'],
            e_rev_I2=IFCondExp2E2I.default_parameters['e_rev_I2'],
            isyn_exc=IFCondExp2E2I.default_parameters['isyn_exc'],
            isyn_exc_2=IFCondExp2E2I.default_parameters['isyn_exc_2'],
            isyn_inh=IFCondExp2E2I.default_parameters['isyn_inh'],
            isyn_inh_2=IFCondExp2E2I.default_parameters['isyn_inh_2']
            ):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IFCondExp2E2IDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label,
            'v_init': v_init, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
            'v_reset': v_reset, 'v_thresh': v_thresh,
            'tau_refrac': tau_refrac,
            'i_offset': i_offset,

            'tau_syn_E': tau_syn_E,
            'tau_syn_E2': tau_syn_E2,
            'tau_syn_I': tau_syn_I,
            'tau_syn_I2': tau_syn_I2,
            'e_rev_E': e_rev_E,
            'e_rev_E2': e_rev_E2,
            'e_rev_I': e_rev_I,
            'e_rev_I2': e_rev_I2,
            'isyn_exc': isyn_exc,
            'isyn_exc_2': isyn_exc_2,
            'isyn_inh': isyn_inh,
            'isyn_inh_2': isyn_inh_2
            })

    @staticmethod
    def build_model():
        return IFCondExp2E2I
