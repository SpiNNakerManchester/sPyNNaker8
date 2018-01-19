from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_control_modules \
    import PushBotLifEthernet
from spynnaker.pyNN.external_devices_models import ExternalDeviceLifControl

_apv_defs = AbstractPopulationVertex.none_pynn_default_parameters


class PushBotLifEthernetDataHolder(DataHolder):
    """ Leaky integrate and fire neuron with an exponentially decaying \
        current input
    """

    def __init__(
            self, protocol, devices, pushbot_ip_address, pushbot_port=56000,

            # default params from abstract pop vertex
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
            v_init=PushBotLifEthernet.none_pynn_default_parameters['v_init']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(PushBotLifEthernetDataHolder, self).__init__({
            'constraints': constraints,
            'devices': devices,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'label': label,
            'protocol': protocol,
            'pushbot_ip_address': pushbot_ip_address,
            'pushbot_port': pushbot_port,
            'ring_buffer_sigma': ring_buffer_sigma,
            'spikes_per_second': spikes_per_second,

            'cm': cm,
            'i_offset': i_offset,
            'tau_m': tau_m,
            'tau_refrac': tau_refrac,
            'tau_syn_E': tau_syn_E,
            'tau_syn_I': tau_syn_I,
            'v_init': v_init,
            'v_reset': v_reset,
            'v_rest': v_rest})

    @staticmethod
    def build_model():
        return PushBotLifEthernet
