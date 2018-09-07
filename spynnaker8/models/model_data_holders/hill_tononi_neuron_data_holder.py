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
            v_thresh_resting=HillTononiNeuron.default_parameters[
                'v_thresh_resting'],
            v_thresh_tau=HillTononiNeuron.default_parameters['v_thresh_tau'],
            v_thresh_Na_reversal=HillTononiNeuron.default_parameters[
                'v_thresh_Na_reversal'],

            # #### Synapse Model ####
            # AMPA - excitatory
            exc_a_response=HillTononiNeuron.default_parameters[
                'exc_a_response'],
            exc_a_A=HillTononiNeuron.default_parameters['exc_a_A'],
            exc_a_tau=HillTononiNeuron.default_parameters['exc_a_tau'],
            exc_b_response=HillTononiNeuron.default_parameters[
                'exc_b_response'],
            exc_b_B=HillTononiNeuron.default_parameters['exc_b_B'],
            exc_b_tau=HillTononiNeuron.default_parameters['exc_b_tau'],

            # NMDA - excitatory2
            exc2_a_response=HillTononiNeuron.default_parameters[
                'exc2_a_response'],
            exc2_a_A=HillTononiNeuron.default_parameters['exc2_a_A'],
            exc2_a_tau=HillTononiNeuron.default_parameters['exc2_a_tau'],
            exc2_b_response=HillTononiNeuron.default_parameters[
                'exc2_b_response'],
            exc2_b_B=HillTononiNeuron.default_parameters['exc2_b_B'],
            exc2_b_tau=HillTononiNeuron.default_parameters['exc2_b_tau'],

            # GABA_A - inhibitory
            inh_a_response=HillTononiNeuron.default_parameters[
                'inh_a_response'],
            inh_a_A=HillTononiNeuron.default_parameters['inh_a_A'],
            inh_a_tau=HillTononiNeuron.default_parameters['inh_a_tau'],
            inh_b_response=HillTononiNeuron.default_parameters[
                'inh_b_response'],
            inh_b_B=HillTononiNeuron.default_parameters['inh_b_B'],
            inh_b_tau=HillTononiNeuron.default_parameters['inh_b_tau'],

            # GABA_B - inhibitory2
            inh2_a_response=HillTononiNeuron.default_parameters[
                'inh2_a_response'],
            inh2_a_A=HillTononiNeuron.default_parameters['inh2_a_A'],
            inh2_a_tau=HillTononiNeuron.default_parameters['inh2_a_tau'],
            inh2_b_response=HillTononiNeuron.default_parameters[
                'inh2_b_response'],
            inh2_b_B=HillTononiNeuron.default_parameters['inh2_b_B'],
            inh2_b_tau=HillTononiNeuron.default_parameters['inh2_b_tau'],

            # #### Input Type ####
            ampa_rev_E=HillTononiNeuron.default_parameters['ampa_rev_E'],
            nmda_rev_E=HillTononiNeuron.default_parameters['nmda_rev_E'],
            gaba_a_rev_E=HillTononiNeuron.default_parameters['gaba_a_rev_E'],
            gaba_b_rev_E=HillTononiNeuron.default_parameters['gaba_b_rev_E'],

            # #### Additional Input ####
            # Pacemaker
            I_H=HillTononiNeuron.default_parameters['I_H'],
            g_H=HillTononiNeuron.default_parameters['g_H'],
            E_H=HillTononiNeuron.default_parameters['E_H'],
            m_H=HillTononiNeuron.default_parameters['m_H'],
            m_inf_H=HillTononiNeuron.default_parameters['m_inf_H'],
            e_to_t_on_tau_m_H=HillTononiNeuron.default_parameters['e_to_t_on_tau_m_H'],
            # Calcium
            I_T=HillTononiNeuron.default_parameters['I_T'],
            g_T=HillTononiNeuron.default_parameters['g_T'],
            E_T=HillTononiNeuron.default_parameters['E_T'],
            m_T=HillTononiNeuron.default_parameters['m_T'],
            m_inf_T=HillTononiNeuron.default_parameters['m_inf_T'],
            e_to_t_on_tau_m_T=HillTononiNeuron.default_parameters['e_to_t_on_tau_m_T'],
            h_T=HillTononiNeuron.default_parameters['h_T'],
            h_inf_T=HillTononiNeuron.default_parameters['h_inf_T'],
            e_to_t_on_tau_h_T=HillTononiNeuron.default_parameters['e_to_t_on_tau_h_T'],
            # Sodium
            I_NaP=HillTononiNeuron.default_parameters['I_NaP'],
            g_NaP=HillTononiNeuron.default_parameters['g_NaP'],
            E_NaP=HillTononiNeuron.default_parameters['E_NaP'],
            m_inf_NaP=HillTononiNeuron.default_parameters['m_inf_NaP'],
            # Potassium
            I_DK=HillTononiNeuron.default_parameters['I_DK'],
            g_DK=HillTononiNeuron.default_parameters['g_DK'],
            E_DK=HillTononiNeuron.default_parameters['E_DK'],
            m_inf_DK=HillTononiNeuron.default_parameters['m_inf_DK'],
            e_to_t_on_tau_m_DK=HillTononiNeuron.default_parameters['e_to_t_on_tau_m_DK'],
            D=HillTononiNeuron.default_parameters['D'],
            D_infinity=HillTononiNeuron.default_parameters['D_infinity'],
            # Voltage Clamp
            v_clamp=HillTononiNeuron.default_parameters['v_clamp'],
            s_clamp=HillTononiNeuron.default_parameters['s_clamp'],
            t_clamp=HillTononiNeuron.default_parameters['t_clamp'],
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

            # #### Input Type ####
            'ampa_rev_E': ampa_rev_E,
            'nmda_rev_E': nmda_rev_E,
            'gaba_a_rev_E': gaba_a_rev_E,
            'gaba_b_rev_E': gaba_b_rev_E,

            # #### Additional Input ####
            # Pacemaker Current
            'I_H': I_H,
            'g_H': g_H,
            'E_H': E_H,
            'm_H': m_H,
            'm_inf_H': m_inf_H,
            'e_to_t_on_tau_m_H': e_to_t_on_tau_m_H,
            # Calcium Current
            'I_T': I_T,
            'g_T': g_T,
            'E_T': E_T,
            'm_T': m_T,
            'm_inf_T': m_inf_T,
            'e_to_t_on_tau_m_T': e_to_t_on_tau_m_T,
            'h_T': h_T,
            'h_inf_T': h_inf_T,
            'e_to_t_on_tau_h_T': e_to_t_on_tau_h_T,
            # Sodium Current
            'I_NaP': I_NaP,
            'g_NaP': g_NaP,
            'E_NaP': E_NaP,
            'm_inf_NaP': m_inf_NaP,
            # Potassium Current
            'I_DK': I_DK,
            'g_DK': g_DK,
            'E_DK': E_DK,
            'm_inf_DK': m_inf_DK,
            'e_to_t_on_tau_m_DK': e_to_t_on_tau_m_DK,
            'D': D,
            'D_infinity': D_infinity,
            # Voltage Clamp
            'v_clamp': v_clamp,
            's_clamp': s_clamp,
            't_clamp': t_clamp
            })

    @staticmethod
    def build_model():
        return HillTononiNeuron
