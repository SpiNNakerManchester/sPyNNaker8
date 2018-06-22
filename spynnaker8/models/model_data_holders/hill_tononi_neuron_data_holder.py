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

            v_thresh=HillTononiNeuron.default_parameters['v_thresh'],
            v_thresh_resting=HillTononiNeuron.default_parameters['v_thresh_resting'],
            v_thresh_tau=HillTononiNeuron.default_parameters['v_thresh_tau'],
            v_thresh_Na_reversal=HillTononiNeuron.default_parameters[
                'v_thresh_Na_reversal'],

            tau_syn_E=HillTononiNeuron.default_parameters['tau_syn_E'],
            tau_syn_I=HillTononiNeuron.default_parameters['tau_syn_I'],
            ):
        # pylint: disable=too-many-arguments, too-many-locals
        super(HillTononiNeuronDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
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

            'v_thresh': v_thresh,
            'v_thresh_resting': v_thresh_resting,
            'v_thresh_tau': v_thresh_tau,
            'v_thresh_Na_reversal': v_thresh_Na_reversal,

            'tau_syn_E': tau_syn_E,
            'tau_syn_I': tau_syn_I,
            })

    @staticmethod
    def build_model():
        return HillTononiNeuron
