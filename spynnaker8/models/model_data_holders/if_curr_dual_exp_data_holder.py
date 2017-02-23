from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base import \
    IFCurrDualExpBase


class IFCurrDualExpDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,
            tau_m=None, cm=None, v_rest=None, v_reset=None, v_thresh=None,
            tau_syn_E=None, tau_syn_E2=None, tau_syn_I=None, tau_refrac=None,
            i_offset=None, v_init=None):
        DataHolder.__init__(
            self,
            {'spikes_per_second': spikes_per_second,
             'ring_buffer_sigma': ring_buffer_sigma, 'label': label,
             'incoming_spike_buffer_size': incoming_spike_buffer_size,
             'constraints': constraints, 'tau_refrac': tau_refrac,
             'tau_m': tau_m, 'tau_syn_E': tau_syn_E, 'cm': cm,
             'v_rest': v_rest, 'v_reset': v_reset, 'v_thresh': v_thresh,
             'tau_syn_E2': tau_syn_E2, 'tau_syn_I': tau_syn_I,
             'i_offset': i_offset, 'v_init': v_init})

    @staticmethod
    def build_model():
        return IFCurrDualExpBase
