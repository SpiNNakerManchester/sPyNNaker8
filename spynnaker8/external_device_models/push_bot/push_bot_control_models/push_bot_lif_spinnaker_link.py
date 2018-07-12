from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_control_modules \
    import PushBotLifSpinnakerLink
from spynnaker.pyNN.external_devices_models import ExternalDeviceLifControl

import logging

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters
logger = logging.getLogger(__name__)


class PushBotLifSpinnakerLinkDataHolder(DataHolder):
    """ Control module for a PushBot connected to a SpiNNaker Link
    """

    def __init__(
            self, protocol, devices,

            spikes_per_second=_apv_defs['spikes_per_second'],
            label=_apv_defs['label'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs[
                'incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],

            # default params for the neuron model type
            tau_m=ExternalDeviceLifControl.default_parameters['tau_m'],
            cm=ExternalDeviceLifControl.default_parameters['cm'],
            v_rest=ExternalDeviceLifControl.default_parameters['v_rest'],
            v_reset=ExternalDeviceLifControl.default_parameters['v_reset'],
            tau_syn_E=ExternalDeviceLifControl.default_parameters['tau_syn_E'],
            tau_syn_I=ExternalDeviceLifControl.default_parameters['tau_syn_I'],
            tau_refrac=ExternalDeviceLifControl.default_parameters[
                'tau_refrac'],
            i_offset=ExternalDeviceLifControl.default_parameters['i_offset'],
            v_init=ExternalDeviceLifControl.initialize_parameters['v_init']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(PushBotLifSpinnakerLinkDataHolder, self).__init__({
            'protocol': protocol, 'devices': devices,
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma, 'label': label,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'tau_m': tau_m, 'cm': cm, 'v_rest': v_rest, 'v_reset': v_reset,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac, 'i_offset': i_offset, 'v_init': v_init})

    @staticmethod
    def build_model():
        return PushBotLifSpinnakerLink
