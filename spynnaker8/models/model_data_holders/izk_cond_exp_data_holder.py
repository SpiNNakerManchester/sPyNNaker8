from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IzkCondExpBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IzkCondExpDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            a=IzkCondExpBase.default_parameters['a'],
            b=IzkCondExpBase.default_parameters['b'],
            c=IzkCondExpBase.default_parameters['c'],
            d=IzkCondExpBase.default_parameters['d'],
            i_offset=IzkCondExpBase.default_parameters['i_offset'],
            u_init=IzkCondExpBase.initialize_parameters['u_init'],
            v_init=IzkCondExpBase.initialize_parameters['v_init'],
            tau_syn_E=IzkCondExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IzkCondExpBase.default_parameters['tau_syn_I'],
            e_rev_E=IzkCondExpBase.default_parameters['e_rev_E'],
            e_rev_I=IzkCondExpBase.default_parameters['e_rev_I'],
            isyn_exc=IzkCondExpBase.default_parameters['isyn_exc'],
            isyn_inh=IzkCondExpBase.default_parameters['isyn_inh']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IzkCondExpDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints, 'label': label, 'a': a, 'b': b,
            'c': c, 'd': d, 'i_offset': i_offset, 'u_init': u_init,
            'v_init': v_init, 'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh, 'e_rev_E': e_rev_E,
            'e_rev_I': e_rev_I})

    @staticmethod
    def build_model():
        return IzkCondExpBase
