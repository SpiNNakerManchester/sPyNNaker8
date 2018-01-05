from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IzkCurrExpBase

_apv_defaults = AbstractPopulationVertex.none_pynn_default_parameters


class IzkCurrExpDataHolder(DataHolder):
    def __init__(
            self,

            spikes_per_second=_apv_defaults['spikes_per_second'],
            ring_buffer_sigma=_apv_defaults['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defaults[
                'incoming_spike_buffer_size'],
            constraints=_apv_defaults['constraints'],
            label=_apv_defaults['label'],

            a=IzkCurrExpBase.default_parameters['a'],
            b=IzkCurrExpBase.default_parameters['b'],
            c=IzkCurrExpBase.default_parameters['c'],
            d=IzkCurrExpBase.default_parameters['d'],
            i_offset=IzkCurrExpBase.default_parameters['i_offset'],
            u_init=IzkCurrExpBase.default_parameters['u_init'],
            v_init=IzkCurrExpBase.default_parameters['v_init'],
            tau_syn_E=IzkCurrExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IzkCurrExpBase.default_parameters['tau_syn_I'],
            isyn_exc=IzkCurrExpBase.default_parameters['isyn_exc'],
            isyn_inh=IzkCurrExpBase.default_parameters['isyn_inh']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IzkCurrExpDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label, 'a': a, 'b': b,
            'c': c, 'd': d, 'i_offset': i_offset, 'u_init': u_init,
            'v_init': v_init, 'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh})

    @staticmethod
    def build_model():
        return IzkCurrExpBase
