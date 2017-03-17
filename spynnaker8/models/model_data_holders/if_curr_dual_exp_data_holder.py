from spynnaker.pyNN.models.neuron.abstract_population_vertex import \
    AbstractPopulationVertex
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base import \
    IFCurrDualExpBase


class IFCurrDualExpDataHolder(DataHolder):
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
            constraints=
            AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],
            label=
            AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],
            tau_m=IFCurrDualExpBase.default_parameters['tau_m'],
            cm=IFCurrDualExpBase.default_parameters['cm'],
            v_rest=IFCurrDualExpBase.default_parameters['v_rest'],
            v_reset=IFCurrDualExpBase.default_parameters['v_reset'],
            v_thresh=IFCurrDualExpBase.default_parameters['v_thresh'],
            tau_syn_E=IFCurrDualExpBase.default_parameters['tau_syn_E'],
            tau_syn_E2=IFCurrDualExpBase.default_parameters['tau_syn_E2'],
            tau_syn_I=IFCurrDualExpBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrDualExpBase.default_parameters['tau_refrac'],
            i_offset=IFCurrDualExpBase.default_parameters['i_offset'],
            v_init=IFCurrDualExpBase.none_pynn_default_parameters['v_init']):
        DataHolder.__init__(
            self,
            {'spikes_per_second': spikes_per_second,
             'ring_buffer_sigma': ring_buffer_sigma, 'label': label,
             'incoming_spike_buffer_size': incoming_spike_buffer_size,
             'constraints': constraints, 'tau_refrac': tau_refrac,
             'tau_m': tau_m, 'tau_syn_E': tau_syn_E, 'cm': cm,
             'v_rest': v_rest, 'v_reset': v_reset, 'v_thresh': v_thresh,
             'tau_syn_E2': tau_syn_E2, 'tau_syn_I': tau_syn_I,
             'i_offset': i_offset, 'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrDualExpBase
