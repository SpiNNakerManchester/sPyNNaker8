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
            tau_refrac=HillTononi.default_parameters['tau_refrac'],
            i_offset=HillTononi.default_parameters['i_offset'],

        # Threshold parameters
            v_thresh=HillTononi.default_parameters['v_thresh'],
            v_thresh_resting=HillTononi.default_parameters['v_thresh_resting'],
            v_thresh_tau=HillTononi.default_parameters['v_thresh_tau'],
            v_thresh_Na_reversal=HillTononi.default_parameters[
                'v_thresh_Na_reversal'],

         # Synapse Type
            # AMPA - excitatory
            exc_a_response=HillTononi.default_parameters['exc_a_response'],
            exc_a_A=HillTononi.default_parameters['exc_a_A'],
            exc_a_tau=HillTononi.default_parameters['exc_a_tau'],
            exc_b_response=HillTononi.default_parameters['exc_b_response'],
            exc_b_B=HillTononi.default_parameters['exc_b_B'],
            exc_b_tau=HillTononi.default_parameters['exc_b_tau'],

            # NMDA - excitatory2
            exc2_a_response=HillTononi.default_parameters['exc2_a_response'],
            exc2_a_A=HillTononi.default_parameters['exc2_a_A'],
            exc2_a_tau=HillTononi.default_parameters['exc2_a_tau'],
            exc2_b_response=HillTononi.default_parameters['exc2_b_response'],
            exc2_b_B=HillTononi.default_parameters['exc2_b_B'],
            exc2_b_tau=HillTononi.default_parameters['exc2_b_tau'],

            # GABA_A - inhibitory
            inh_a_response=HillTononi.default_parameters['inh_a_response'],
            inh_a_A=HillTononi.default_parameters['inh_a_A'],
            inh_a_tau=HillTononi.default_parameters['inh_a_tau'],
            inh_b_response=HillTononi.default_parameters['inh_b_response'],
            inh_b_B=HillTononi.default_parameters['inh_b_B'],
            inh_b_tau=HillTononi.default_parameters['inh_b_tau'],

            # GABA_B - inhibitory2
            inh2_a_response=HillTononi.default_parameters['inh2_a_response'],
            inh2_a_A=HillTononi.default_parameters['inh2_a_A'],
            inh2_a_tau=HillTononi.default_parameters['inh2_a_tau'],
            inh2_b_response=HillTononi.default_parameters['inh2_b_response'],
            inh2_b_B=HillTononi.default_parameters['inh2_b_B'],
            inh2_b_tau=HillTononi.default_parameters['inh2_b_tau'],

        # Input Type
#             e_rev_AMPA=HillTononi.default_parameters['e_rev_AMPA'],
#             e_rev_NMDA=HillTononi.default_parameters['e_rev_NMDA'],
#             e_rev_GABA_A=HillTononi.default_parameters['e_rev_GABA_A'],
#             e_rev_GABA_B=HillTononi.default_parameters['e_rev_GABA_B']


            ):
        DataHolder.__init__(
            self, {
                'spikes_per_second': spikes_per_second,
                'ring_buffer_sigma': ring_buffer_sigma,
                'incoming_spike_buffer_size': incoming_spike_buffer_size,
                'constraints': constraints,

                'label': label, 'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest,
                'v_reset': v_reset,

            # Threshold Type
                'v_thresh': v_thresh,

            # Synapse Type
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

            # Input Type
#                 'e_rev_AMPA': e_rev_AMPA,
#                 'e_rev_NMDA': e_rev_NMDA,
#                 'e_rev_GABA_A': e_rev_GABA_A,
#                 'e_rev_GABA_B': e_rev_GABA_B,

                'tau_refrac': tau_refrac, 'i_offset': i_offset,
                'v_init': v_init})

    @staticmethod
    def build_model():
        return HillTononi
