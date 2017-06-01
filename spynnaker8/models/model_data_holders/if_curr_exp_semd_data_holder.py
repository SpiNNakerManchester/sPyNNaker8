from spynnaker.pyNN.models.neuron.abstract_population_vertex import \
    AbstractPopulationVertex
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_semd_base import \
    IFCurrExpSEMDBase


class IFCurrExpSEMDDataHolder(DataHolder):
    def __init__(
            self,

            spikes_per_second=AbstractPopulationVertex.
            none_pynn_default_parameters['spikes_per_second'],

            ring_buffer_sigma=AbstractPopulationVertex.
            none_pynn_default_parameters['ring_buffer_sigma'],

            incoming_spike_buffer_size=AbstractPopulationVertex.
            none_pynn_default_parameters['incoming_spike_buffer_size'],

            constraints=AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],

            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],

            v_init=IFCurrExpSEMDBase.none_pynn_default_parameters['v_init'],
            tau_m=IFCurrExpSEMDBase.default_parameters['tau_m'],
            cm=IFCurrExpSEMDBase.default_parameters['cm'],
            v_rest=IFCurrExpSEMDBase.default_parameters['v_rest'],
            v_reset=IFCurrExpSEMDBase.default_parameters['v_reset'],
            v_thresh=IFCurrExpSEMDBase.default_parameters['v_thresh'],
            tau_syn_E=IFCurrExpSEMDBase.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrExpSEMDBase.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrExpSEMDBase.default_parameters['tau_refrac'],
            i_offset=IFCurrExpSEMDBase.default_parameters['i_offset'],
            multiplicator=
            IFCurrExpSEMDBase.default_parameters['multiplicator'],
            inh_input_previous=
            IFCurrExpSEMDBase.default_parameters['inh_input_previous']):
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
                'multiplicator': multiplicator,
                'inh_input_previous': inh_input_previous, 'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrExpSEMDBase
