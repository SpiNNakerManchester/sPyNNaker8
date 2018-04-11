from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCondExpCa2Concentration


class IfCondExpCa2ConcentrationDataHolder(DataHolder):

    def __init__(
            self, spikes_per_second=AbstractPopulationVertex.
            non_pynn_default_parameters['spikes_per_second'],
            ring_buffer_sigma=AbstractPopulationVertex.
            non_pynn_default_parameters['ring_buffer_sigma'],
            incoming_spike_buffer_size=AbstractPopulationVertex.
            non_pynn_default_parameters['incoming_spike_buffer_size'],
            constraints=AbstractPopulationVertex.non_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.non_pynn_default_parameters[
                'label'],
            tau_m=IFCondExpCa2Concentration.default_parameters['tau_m'],
            cm=IFCondExpCa2Concentration.default_parameters['cm'],
            v_rest=IFCondExpCa2Concentration.default_parameters['v_rest'],
            v_reset=IFCondExpCa2Concentration.default_parameters['v_reset'],
            v_thresh=IFCondExpCa2Concentration.default_parameters['v_thresh'],
            tau_syn_E=IFCondExpCa2Concentration.default_parameters['tau_syn_E'],
            tau_syn_I=IFCondExpCa2Concentration.default_parameters['tau_syn_I'],
            tau_refrac=IFCondExpCa2Concentration.default_parameters['tau_refrac'],
            i_offset=IFCondExpCa2Concentration.default_parameters['i_offset'],
            tau_ca2=IFCondExpCa2Concentration.default_parameters["tau_ca2"],
            i_ca2=IFCondExpCa2Concentration.default_parameters["i_ca2"],
            i_alpha=IFCondExpCa2Concentration.default_parameters["i_alpha"],
            v_init=IFCondExpCa2Concentration.initialize_parameters['v_init'],
            isyn_exc=IFCondExpCa2Concentration.default_parameters['isyn_exc'],
            isyn_inh=IFCondExpCa2Concentration.default_parameters['isyn_inh'],
            e_rev_E=IFCondExpCa2Concentration.default_parameters['e_rev_E'],
            e_rev_I=IFCondExpCa2Concentration.default_parameters['e_rev_I']):
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
        return IFCondExpCa2Concentration
