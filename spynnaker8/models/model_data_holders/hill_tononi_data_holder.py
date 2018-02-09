from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import HillTononi


class HillTononiDataHolder(DataHolder):
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

            v_init=HillTononi.none_pynn_default_parameters['v_init'],
            tau_m=HillTononi.default_parameters['tau_m'],
            cm=HillTononi.default_parameters['cm'],
            v_rest=HillTononi.default_parameters['v_rest'],
            v_reset=HillTononi.default_parameters['v_reset'],

            # Threshold parameters
            v_thresh=HillTononi.default_parameters['v_thresh'],
            v_thresh_resting=HillTononi.default_parameters['v_thresh_resting'],
            v_thresh_tau=HillTononi.default_parameters['v_thresh_tau'],
            v_thresh_Na_reversal=HillTononi.default_parameters[
                'v_thresh_Na_reversal'],

            tau_syn_E=HillTononi.default_parameters['tau_syn_E'],
            tau_syn_I=HillTononi.default_parameters['tau_syn_I'],

            tau_refrac=HillTononi.default_parameters['tau_refrac'],
            i_offset=HillTononi.default_parameters['i_offset']):
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
        return HillTononi
