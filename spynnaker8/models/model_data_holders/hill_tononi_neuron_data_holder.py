from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import HillTononiNeuron

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class HillTononiNeuronDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            # #### Neuron Model ####
            v_init=HillTononiNeuron.initialize_parameters['v_init'],
            g_Na=HillTononiNeuron.default_parameters['g_Na'],
            E_Na=HillTononiNeuron.default_parameters['E_Na'],
            g_K=HillTononiNeuron.default_parameters['g_K'],
            E_K=HillTononiNeuron.default_parameters['E_K'],
            tau_m=HillTononiNeuron.default_parameters['tau_m'],
            i_offset=HillTononiNeuron.default_parameters['i_offset'],
            g_spike=HillTononiNeuron.default_parameters['g_spike'],
            tau_spike=HillTononiNeuron.default_parameters['tau_spike'],
            t_spike=HillTononiNeuron.default_parameters['t_spike'],

            # #### Threshold Model ####
            v_thresh=HillTononiNeuron.default_parameters['v_thresh'],
            v_thresh_resting=HillTononiNeuron.default_parameters['v_thresh_resting'],
            v_thresh_tau=HillTononiNeuron.default_parameters['v_thresh_tau'],
            v_thresh_Na_reversal=HillTononiNeuron.default_parameters[
                'v_thresh_Na_reversal'],

            # #### Synapse Model ####
            # AMPA - excitatory
            exc_a_response=HillTononiNeuron.default_parameters['exc_a_response'],
            exc_a_A=HillTononiNeuron.default_parameters['exc_a_A'],
            exc_a_tau=HillTononiNeuron.default_parameters['exc_a_tau'],
            exc_b_response=HillTononiNeuron.default_parameters['exc_b_response'],
            exc_b_B=HillTononiNeuron.default_parameters['exc_b_B'],
            exc_b_tau=HillTononiNeuron.default_parameters['exc_b_tau'],

            # NMDA - excitatory2
            exc2_a_response=HillTononiNeuron.default_parameters['exc2_a_response'],
            exc2_a_A=HillTononiNeuron.default_parameters['exc2_a_A'],
            exc2_a_tau=HillTononiNeuron.default_parameters['exc2_a_tau'],
            exc2_b_response=HillTononiNeuron.default_parameters['exc2_b_response'],
            exc2_b_B=HillTononiNeuron.default_parameters['exc2_b_B'],
            exc2_b_tau=HillTononiNeuron.default_parameters['exc2_b_tau'],

            # GABA_A - inhibitory
            inh_a_response=HillTononiNeuron.default_parameters['inh_a_response'],
            inh_a_A=HillTononiNeuron.default_parameters['inh_a_A'],
            inh_a_tau=HillTononiNeuron.default_parameters['inh_a_tau'],
            inh_b_response=HillTononiNeuron.default_parameters['inh_b_response'],
            inh_b_B=HillTononiNeuron.default_parameters['inh_b_B'],
            inh_b_tau=HillTononiNeuron.default_parameters['inh_b_tau'],

            # GABA_B - inhibitory2
            inh2_a_response=HillTononiNeuron.default_parameters['inh2_a_response'],
            inh2_a_A=HillTononiNeuron.default_parameters['inh2_a_A'],
            inh2_a_tau=HillTononiNeuron.default_parameters['inh2_a_tau'],
            inh2_b_response=HillTononiNeuron.default_parameters['inh2_b_response'],
            inh2_b_B=HillTononiNeuron.default_parameters['inh2_b_B'],
            inh2_b_tau=HillTononiNeuron.default_parameters['inh2_b_tau'],

            ):

        # pylint: disable=too-many-arguments, too-many-locals
        super(HillTononiNeuronDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,

            # #### Neuron Model ####
            'v_init': v_init,
            'g_Na': g_Na,
            'E_Na': E_Na,
            'g_K': g_K,
            'E_K': E_K,
            'tau_m': tau_m,
            'i_offset': i_offset,

            'g_spike': g_spike,
            'tau_spike': tau_spike,
            't_spike': t_spike,

            # #### Threshold ####
            'v_thresh': v_thresh,
            'v_thresh_resting': v_thresh_resting,
            'v_thresh_tau': v_thresh_tau,
            'v_thresh_Na_reversal': v_thresh_Na_reversal,

            # #### Synapse Model ####
            'exc_a_response': exc_a_response,
            'exc_a_A': exc_a_A,
            'exc_a_tau': exc_a_tau,
            'exc_b_response': exc_b_response,
            'exc_b_B': exc_b_B,
            'exc_b_tau': exc_b_tau,
            # NMDA - excitatory2
            'exc2_a_response': exc2_a_response,
            'exc2_a_A': exc2_a_A,
            'exc2_a_tau': exc2_a_tau,
            'exc2_b_response': exc2_b_response,
            'exc2_b_B': exc2_b_B,
            'exc2_b_tau': exc2_b_tau,
            # GABA_A - inhibitory
            'inh_a_response': inh_a_response,
            'inh_a_A': inh_a_A,
            'inh_a_tau': inh_a_tau,
            'inh_b_response': inh_b_response,
            'inh_b_B': inh_b_B,
            'inh_b_tau': inh_b_tau,
            # GABA_B - inhibitory2
            'inh2_a_response': inh2_a_response,
            'inh2_a_A': inh2_a_A,
            'inh2_a_tau': inh2_a_tau,
            'inh2_b_response': inh2_b_response,
            'inh2_b_B': inh2_b_B,
            'inh2_b_tau': inh2_b_tau,

            })

    @staticmethod
    def build_model():
        return HillTononiNeuron
