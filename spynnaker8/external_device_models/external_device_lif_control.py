from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import ExternalDeviceLifControl


class ExternalDeviceLifControlDataHolder(DataHolder):
    """ Leaky integrate and fire neuron with an exponentially decaying \
        current input
    """

    def __init__(
            self, devices, create_edges, translator=None,

            # default params from abstract pop vertex
            spikes_per_second=AbstractPopulationVertex.
            non_pynn_default_parameters['spikes_per_second'],
            label=AbstractPopulationVertex.non_pynn_default_parameters[
                'label'],
            ring_buffer_sigma=AbstractPopulationVertex.
            non_pynn_default_parameters['ring_buffer_sigma'],
            incoming_spike_buffer_size=AbstractPopulationVertex.
            non_pynn_default_parameters['incoming_spike_buffer_size'],
            constraints=AbstractPopulationVertex.
            non_pynn_default_parameters['constraints'],

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
            v_init=ExternalDeviceLifControl.initialize_parameters[
                'v_init'],
            isyn_inh=ExternalDeviceLifControl.default_parameters['isyn_inh'],
            isyn_exc=ExternalDeviceLifControl.default_parameters['isyn_exc']):
        # pylint: disable=too-many-arguments, too-many-locals
        super(ExternalDeviceLifControlDataHolder, self).__init__({
            'constraints': constraints,
            'create_edges': create_edges,
            'devices': devices,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'label': label,
            'ring_buffer_sigma': ring_buffer_sigma,
            'spikes_per_second': spikes_per_second,
            'translator': translator,

            'cm': cm,
            'i_offset': i_offset,
            'isyn_exc': isyn_exc,
            'isyn_inh': isyn_inh,
            'tau_m': tau_m,
            'tau_syn_E': tau_syn_E,
            'tau_syn_I': tau_syn_I,
            'tau_refrac': tau_refrac,
            'v_init': v_init,
            'v_reset': v_reset,
            'v_rest': v_rest})

    @staticmethod
    def build_model():
        return ExternalDeviceLifControl
