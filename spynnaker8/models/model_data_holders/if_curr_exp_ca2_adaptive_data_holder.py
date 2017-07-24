from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrExpCa2Adaptive


class IfCurrExpCa2AdaptiveDataHolder(DataHolder):

    def __init__(
            self, spikes_per_second=AbstractPopulationVertex.
            none_pynn_default_parameters['spikes_per_second'],
            ring_buffer_sigma=AbstractPopulationVertex.
            none_pynn_default_parameters['ring_buffer_sigma'],
            incoming_spike_buffer_size=AbstractPopulationVertex.
            none_pynn_default_parameters['incoming_spike_buffer_size'],
            constraints=AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],
            tau_m=IFCurrExpCa2Adaptive.default_parameters['tau_m'],
            cm=IFCurrExpCa2Adaptive.default_parameters['cm'],
            v_rest=IFCurrExpCa2Adaptive.default_parameters['v_rest'],
            v_reset=IFCurrExpCa2Adaptive.default_parameters['v_reset'],
            v_thresh=IFCurrExpCa2Adaptive.default_parameters['v_thresh'],
            tau_syn_E=IFCurrExpCa2Adaptive.default_parameters['tau_syn_E'],
            tau_syn_I=IFCurrExpCa2Adaptive.default_parameters['tau_syn_I'],
            tau_refrac=IFCurrExpCa2Adaptive.default_parameters['tau_refrac'],
            i_offset=IFCurrExpCa2Adaptive.default_parameters['i_offset'],
            tau_ca2=IFCurrExpCa2Adaptive.default_parameters["tau_ca2"],
            i_ca2=IFCurrExpCa2Adaptive.default_parameters["i_ca2"],
            i_alpha=IFCurrExpCa2Adaptive.default_parameters["i_alpha"],
            v_init=IFCurrExpCa2Adaptive.none_pynn_default_parameters['v_init'],
            isyn_exc=IFCurrExpCa2Adaptive.default_parameters['isyn_exc'],
            isyn_inh=IFCurrExpCa2Adaptive.default_parameters['isyn_inh']):
        DataHolder.__init__(
            self,
            {
                'spikes_per_second': spikes_per_second,
                'ring_buffer_sigma': ring_buffer_sigma,
                'incoming_spike_buffer_size': incoming_spike_buffer_size,
                'constraints': constraints, 'label': label,
                'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
                'v_reset': v_reset, 'v_thresh': v_thresh,
                'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
                'tau_refrac': tau_refrac, 'i_offset': i_offset,
                'v_init': v_init, 'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
                'tau_ca2': tau_ca2, 'i_ca2': i_ca2, 'i_alpha': i_alpha})

    @staticmethod
    def build_model():
        return IFCurrExpCa2Adaptive
