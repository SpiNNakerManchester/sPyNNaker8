from spynnaker.pyNN.models.neuron.abstract_population_vertex import \
    AbstractPopulationVertex
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base \
    import IzkCurrExpBase


class IzkCurrExpDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=
            AbstractPopulationVertex.none_pynn_default_parameters[
                'spikes_per_second'],
            ring_buffer_sigma=
            AbstractPopulationVertex.none_pynn_default_parameters[
                'ring_buffer_sigma'],
            incoming_spike_buffer_size=
            AbstractPopulationVertex.none_pynn_default_parameters[
                'incoming_spike_buffer_size'],
            constraints=AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],
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
        DataHolder.__init__(
            self,
            {'spikes_per_second': spikes_per_second,
             'ring_buffer_sigma': ring_buffer_sigma,
             'incoming_spike_buffer_size': incoming_spike_buffer_size,
             'constraints': constraints, 'label': label, 'a': a, 'b': b,
             'c': c, 'd': d, 'i_offset': i_offset, 'u_init': u_init,
             'v_init': v_init, 'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
             'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh})

    @staticmethod
    def build_model():
        return IzkCurrExpBase
