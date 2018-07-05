from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.neuron.builds import IzkCurrCombExp4E4I

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IzkCurrCombExp4E4IDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,

            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],

            a=IzkCurrCombExp4E4I.default_parameters['a'],
            b=IzkCurrCombExp4E4I.default_parameters['b'],
            c=IzkCurrCombExp4E4I.default_parameters['c'],
            d=IzkCurrCombExp4E4I.default_parameters['d'],
            i_offset=IzkCurrCombExp4E4I.default_parameters['i_offset'],
            u_init=IzkCurrCombExp4E4I.initialize_parameters['u_init'],
            v_init=IzkCurrCombExp4E4I.initialize_parameters['v_init'],


            ##### synapse parameters #####
            # excitatory
            exc_a_response = IzkCurrCombExp4E4I.default_parameters['exc_a_response'],
            exc_a_A = IzkCurrCombExp4E4I.default_parameters['exc_a_A'],
            exc_a_tau = IzkCurrCombExp4E4I.default_parameters['exc_a_tau'],
            exc_b_response = IzkCurrCombExp4E4I.default_parameters['exc_b_response'],
            exc_b_B = IzkCurrCombExp4E4I.default_parameters['exc_b_B'],
            exc_b_tau = IzkCurrCombExp4E4I.default_parameters['exc_b_tau'],

            # excitatory2
            exc2_a_response = IzkCurrCombExp4E4I.default_parameters['exc2_a_response'],
            exc2_a_A = IzkCurrCombExp4E4I.default_parameters['exc2_a_A'],
            exc2_a_tau = IzkCurrCombExp4E4I.default_parameters['exc2_a_tau'],
            exc2_b_response = IzkCurrCombExp4E4I.default_parameters['exc2_b_response'],
            exc2_b_B = IzkCurrCombExp4E4I.default_parameters['exc2_b_B'],
            exc2_b_tau = IzkCurrCombExp4E4I.default_parameters['exc2_b_tau'],

            # excitatory3
            exc3_a_response = IzkCurrCombExp4E4I.default_parameters['exc3_a_response'],
            exc3_a_A = IzkCurrCombExp4E4I.default_parameters['exc3_a_A'],
            exc3_a_tau = IzkCurrCombExp4E4I.default_parameters['exc3_a_tau'],
            exc3_b_response = IzkCurrCombExp4E4I.default_parameters['exc3_b_response'],
            exc3_b_B = IzkCurrCombExp4E4I.default_parameters['exc3_b_B'],
            exc3_b_tau = IzkCurrCombExp4E4I.default_parameters['exc3_b_tau'],

            # excitatory4
            exc4_a_response = IzkCurrCombExp4E4I.default_parameters['exc4_a_response'],
            exc4_a_A = IzkCurrCombExp4E4I.default_parameters['exc4_a_A'],
            exc4_a_tau = IzkCurrCombExp4E4I.default_parameters['exc4_a_tau'],
            exc4_b_response = IzkCurrCombExp4E4I.default_parameters['exc4_b_response'],
            exc4_b_B = IzkCurrCombExp4E4I.default_parameters['exc4_b_B'],
            exc4_b_tau = IzkCurrCombExp4E4I.default_parameters['exc4_b_tau'],

            # inhibitory
            inh_a_response = IzkCurrCombExp4E4I.default_parameters['inh_a_response'],
            inh_a_A = IzkCurrCombExp4E4I.default_parameters['inh_a_A'],
            inh_a_tau = IzkCurrCombExp4E4I.default_parameters['inh_a_tau'],
            inh_b_response = IzkCurrCombExp4E4I.default_parameters['inh_b_response'],
            inh_b_B = IzkCurrCombExp4E4I.default_parameters['inh_b_B'],
            inh_b_tau = IzkCurrCombExp4E4I.default_parameters['inh_b_tau'],

            # inhibitory2
            inh2_a_response = IzkCurrCombExp4E4I.default_parameters['inh2_a_response'],
            inh2_a_A = IzkCurrCombExp4E4I.default_parameters['inh2_a_A'],
            inh2_a_tau = IzkCurrCombExp4E4I.default_parameters['inh2_a_tau'],
            inh2_b_response = IzkCurrCombExp4E4I.default_parameters['inh2_b_response'],
            inh2_b_B = IzkCurrCombExp4E4I.default_parameters['inh2_b_B'],
            inh2_b_tau = IzkCurrCombExp4E4I.default_parameters['inh2_b_tau'],

            # inhibitory3
            inh3_a_response = IzkCurrCombExp4E4I.default_parameters['inh3_a_response'],
            inh3_a_A = IzkCurrCombExp4E4I.default_parameters['inh3_a_A'],
            inh3_a_tau = IzkCurrCombExp4E4I.default_parameters['inh3_a_tau'],
            inh3_b_response = IzkCurrCombExp4E4I.default_parameters['inh3_b_response'],
            inh3_b_B = IzkCurrCombExp4E4I.default_parameters['inh3_b_B'],
            inh3_b_tau = IzkCurrCombExp4E4I.default_parameters['inh3_b_tau'],

            # inhibitory4
            inh4_a_response = IzkCurrCombExp4E4I.default_parameters['inh4_a_response'],
            inh4_a_A = IzkCurrCombExp4E4I.default_parameters['inh4_a_A'],
            inh4_a_tau = IzkCurrCombExp4E4I.default_parameters['inh4_a_tau'],
            inh4_b_response = IzkCurrCombExp4E4I.default_parameters['inh4_b_response'],
            inh4_b_B = IzkCurrCombExp4E4I.default_parameters['inh4_b_B'],
            inh4_b_tau = IzkCurrCombExp4E4I.default_parameters['inh4_b_tau'],


            ):
        # pylint: disable=too-many-arguments, too-many-locals
        super(IzkCurrCombExp4E4IDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'a': a, 'b': b,
            'c': c, 'd': d,
            'i_offset': i_offset,
            'u_init': u_init, 'v_init': v_init,

            ##### synapse parameters #####
            # excitatory
            'exc_a_response':exc_a_response,
            'exc_a_A':exc_a_A,
            'exc_a_tau':exc_a_tau,
            'exc_b_response':exc_b_response,
            'exc_b_B':exc_b_B,
            'exc_b_tau':exc_b_tau,

            # excitatory2
            'exc2_a_response':exc2_a_response,
            'exc2_a_A':exc2_a_A,
            'exc2_a_tau':exc2_a_tau,
            'exc2_b_response':exc2_b_response,
            'exc2_b_B':exc2_b_B,
            'exc2_b_tau':exc2_b_tau,

            # excitatory3
            'exc3_a_response':exc3_a_response,
            'exc3_a_A':exc3_a_A,
            'exc3_a_tau':exc3_a_tau,
            'exc3_b_response':exc3_b_response,
            'exc3_b_B':exc3_b_B,
            'exc3_b_tau':exc3_b_tau,

            # excitatory4
            'exc4_a_response':exc4_a_response,
            'exc4_a_A':exc4_a_A,
            'exc4_a_tau':exc4_a_tau,
            'exc4_b_response':exc4_b_response,
            'exc4_b_B':exc4_b_B,
            'exc4_b_tau':exc4_b_tau,

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
            'inh2_b_tau':inh2_b_tau,

            # inhibitory3
            'inh3_a_response':inh3_a_response,
            'inh3_a_A':inh3_a_A,
            'inh3_a_tau':inh3_a_tau,
            'inh3_b_response':inh3_b_response,
            'inh3_b_B':inh3_b_B,
            'inh3_b_tau':inh3_b_tau,

            # inhibitory4
            'inh4_a_response':inh4_a_response,
            'inh4_a_A':inh4_a_A,
            'inh4_a_tau':inh4_a_tau,
            'inh4_b_response':inh4_b_response,
            'inh4_b_B':inh4_b_B,
            'inh4_b_tau':inh4_b_tau,


            })

    @staticmethod
    def build_model():
        return IzkCurrCombExp4E4I
