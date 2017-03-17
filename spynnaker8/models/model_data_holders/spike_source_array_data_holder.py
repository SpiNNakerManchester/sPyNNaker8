from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.spike_source.spike_source_array \
    import SpikeSourceArray
from spynnaker.pyNN.utilities import constants


class SpikeSourceArrayDataHolder(DataHolder):
    def __init__(
            self, 
            spike_times=SpikeSourceArray.default_parameters['spike_times'],
            port=SpikeSourceArray.none_pynn_default_parameters['port'],
            tag=SpikeSourceArray.none_pynn_default_parameters['tag'],
            ip_address=SpikeSourceArray.none_pynn_default_parameters[
                'ip_address'],
            board_address=SpikeSourceArray.none_pynn_default_parameters[
                'board_address'],
            max_on_chip_memory_usage_for_spikes_in_bytes=
            SpikeSourceArray.none_pynn_default_parameters[
                'max_on_chip_memory_usage_for_spikes_in_bytes'],
            space_before_notification=
            SpikeSourceArray.none_pynn_default_parameters[
                'space_before_notification'],
            constraints=SpikeSourceArray.none_pynn_default_parameters[
                'constraints'],
            label=SpikeSourceArray.none_pynn_default_parameters[
                'label'],
            spike_recorder_buffer_size=
            SpikeSourceArray.none_pynn_default_parameters[
                'spike_recorder_buffer_size'],
            buffer_size_before_receive=
            SpikeSourceArray.none_pynn_default_parameters[
                'buffer_size_before_receive']):
        DataHolder.__init__(
            self, {
                'spike_times': spike_times, 'port': port, 'tag': tag,
                'ip_address': ip_address, 'board_address': board_address,
                'max_on_chip_memory_usage_for_spikes_in_bytes':
                    max_on_chip_memory_usage_for_spikes_in_bytes,
                'space_before_notification': space_before_notification,
                'constraints': constraints, 'label': label,
                'spike_recorder_buffer_size': spike_recorder_buffer_size,
                'buffer_size_before_receive': buffer_size_before_receive})

    @staticmethod
    def build_model():
        return SpikeSourceArray
