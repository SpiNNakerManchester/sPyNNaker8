from spynnaker.pyNN.models.neuron.abstract_population_vertex import \
    AbstractPopulationVertex
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base import IFCurrExpBase

class IFCurrExpDataHolder(DataHolder):
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
            v_init=IFCurrExpBase.none_pynn_default_parameters['v_init'],
            tau_m=IFCurrExpBase.default_parameters['tau_m'],
            cm=IFCurrExpBase.default_parameters['cm'],
            v_rest=IFCurrExpBase.default_parameters['v_rest'],
            v_reset=IFCurrExpBase.default_parameters['v_reset'],
            v_thresh=IFCurrExpBase.default_parameters['v_thresh'],
            tau_syn_E=IFCurrExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrExpBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrExpBase.default_parameters['tau_refrac'],
            i_offset=IFCurrExpBase.default_parameters['i_offset']):
        DataHolder.__init__(
            self, {
                'spikes_per_second': spikes_per_second,
                'ring_buffer_sigma': ring_buffer_sigma,
                'incoming_spike_buffer_size': incoming_spike_buffer_size,
                'constraints': constraints,
                'label': label, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
                'v_reset': v_reset, 'v_thresh': v_thresh,
                'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
                'tau_refrac': tau_refrac, 'i_offset': i_offset,
                'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrExpBase
