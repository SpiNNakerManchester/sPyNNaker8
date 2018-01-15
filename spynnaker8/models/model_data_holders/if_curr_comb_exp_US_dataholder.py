from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IFCurrCombExpUS


class IFCurrCombExpUSDataHolder(DataHolder):
    def __init__(
            self,

            spikes_per_second=AbstractPopulationVertex.
            none_pynn_default_parameters['spikes_per_second'],

            ring_buffer_sigma=AbstractPopulationVertex.
            none_pynn_default_parameters['ring_buffer_sigma'],

            incoming_spike_buffer_size=AbstractPopulationVertex.
            none_pynn_default_parameters['incoming_spike_buffer_size'],

            constraints=AbstractPopulationVertex.
            none_pynn_default_parameters['constraints'],

            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],

            # Neuron parameters
            tau_m=IFCurrCombExpUS.default_parameters['tau_m'],
            cm=IFCurrCombExpUS.default_parameters['cm'],
            v_rest=IFCurrCombExpUS.default_parameters['v_rest'],
            v_reset=IFCurrCombExpUS.default_parameters['v_reset'],
            v_thresh=IFCurrCombExpUS.default_parameters['v_thresh'],
            i_offset=IFCurrCombExpUS.default_parameters['i_offset'],
            v_init=IFCurrCombExpUS.none_pynn_default_parameters['v_init'],
            tau_refrac=IFCurrCombExpUS.default_parameters['tau_refrac'],

            # Compartement defaults
            V_compartment1=IFCurrCombExpUS.default_parameters['V_compartment1'],
            C_compartment1=IFCurrCombExpUS.default_parameters['C_compartment1'],

            ##### synapse parameters #####
            # excitatory
            exc_a_response=IFCurrCombExpUS.default_parameters['exc_a_response'],
            exc_a_A=IFCurrCombExpUS.default_parameters['exc_a_A'],
            exc_a_tau=IFCurrCombExpUS.default_parameters['exc_a_tau'],
            exc_b_response=IFCurrCombExpUS.default_parameters['exc_b_response'],
            exc_b_B=IFCurrCombExpUS.default_parameters['exc_b_B'],
            exc_b_tau=IFCurrCombExpUS.default_parameters['exc_b_tau'],
            # excitatory2
            exc2_a_response=IFCurrCombExpUS.default_parameters['exc2_a_response'],
            exc2_a_A=IFCurrCombExpUS.default_parameters['exc2_a_A'],
            exc2_a_tau=IFCurrCombExpUS.default_parameters['exc2_a_tau'],
            exc2_b_response=IFCurrCombExpUS.default_parameters['exc2_b_response'],
            exc2_b_B=IFCurrCombExpUS.default_parameters['exc2_b_B'],
            exc2_b_tau=IFCurrCombExpUS.default_parameters['exc2_b_tau'],
            # inhibitory
            inh_a_response=IFCurrCombExpUS.default_parameters['inh_a_response'],
            inh_a_A=IFCurrCombExpUS.default_parameters['inh_a_A'],
            inh_a_tau=IFCurrCombExpUS.default_parameters['inh_a_tau'],
            inh_b_response=IFCurrCombExpUS.default_parameters['inh_b_response'],
            inh_b_B=IFCurrCombExpUS.default_parameters['inh_b_B'],
            inh_b_tau=IFCurrCombExpUS.default_parameters['inh_b_tau'],
            # inhibitory2
            inh2_a_response=IFCurrCombExpUS.default_parameters['inh2_a_response'],
            inh2_a_A=IFCurrCombExpUS.default_parameters['inh2_a_A'],
            inh2_a_tau=IFCurrCombExpUS.default_parameters['inh2_a_tau'],
            inh2_b_response=IFCurrCombExpUS.default_parameters['inh2_b_response'],
            inh2_b_B=IFCurrCombExpUS.default_parameters['inh2_b_B'],
            inh2_b_tau=IFCurrCombExpUS.default_parameters['inh2_b_tau']
            ):

        DataHolder.__init__(
            self,
            {'spikes_per_second': spikes_per_second,
             'ring_buffer_sigma': ring_buffer_sigma,
             'label': label,
             'incoming_spike_buffer_size': incoming_spike_buffer_size,
             'constraints': constraints,

             #### Neuron params ####
             'tau_refrac': tau_refrac,
             'tau_m': tau_m,
             'cm': cm,
             'v_rest': v_rest,
             'v_reset': v_reset,
             'v_thresh': v_thresh,
             'i_offset': i_offset,
             'v_init': v_init,

             # Compartement defaults
             'V_compartment1':V_compartment1,
             'C_compartment1':C_compartment1,

             #### Synapse params ####
             # excitatory
             'exc_a_response':exc_a_response,
             'exc_a_A':exc_a_A,
             'exc_a_tau': exc_a_tau,
             'exc_b_response':exc_b_response,
             'exc_b_B':exc_b_B,
             'exc_b_tau': exc_b_tau,
             # excitatory2
             'exc2_a_response':exc2_a_response,
             'exc2_a_A':exc2_a_A,
             'exc2_a_tau':exc2_a_tau,
             'exc2_b_response':exc2_b_response,
             'exc2_b_B':exc2_b_B,
             'exc2_b_tau':exc2_b_tau,
             # inhibitory
             'inh_a_response':inh_a_response,
             'inh_a_A':inh_a_A,
             'inh_a_tau':inh_a_tau,
             'inh_b_response':inh_b_response,
             'inh_b_B':inh_b_B,
             'inh_b_tau':inh_b_tau,
             # inhibitory2
             'inh2_a_response':inh2_a_response,
             'inh2_a_A':inh2_a_A,
             'inh2_a_tau':inh2_a_tau,
             'inh2_b_response':inh2_b_response,
             'inh2_b_B':inh2_b_B,
             'inh2_b_tau':inh2_b_tau
             })

    @staticmethod
    def build_model():
        return IFCurrCombExpUS