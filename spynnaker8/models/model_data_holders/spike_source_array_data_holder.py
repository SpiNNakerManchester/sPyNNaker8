from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.spike_source import SpikeSourceArray

_defaults = SpikeSourceArray.non_pynn_default_parameters


class SpikeSourceArrayDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,
            spike_times=SpikeSourceArray.default_parameters['spike_times'],
            port=_defaults['port'],
            tag=_defaults['tag'],
            ip_address=_defaults['ip_address'],
            board_address=_defaults['board_address'],
            max_on_chip_memory_usage_for_spikes_in_bytes=_defaults[
                'max_on_chip_memory_usage_for_spikes_in_bytes'],
            space_before_notification=_defaults['space_before_notification'],
            constraints=_defaults['constraints'],
            label=_defaults['label'],
            spike_recorder_buffer_size=_defaults['spike_recorder_buffer_size'],
            buffer_size_before_receive=_defaults[
                'buffer_size_before_receive']):
        # pylint: disable=too-many-arguments
        super(SpikeSourceArrayDataHolder, self).__init__({
            'spike_times': spike_times, 'port': port, 'tag': tag,
            'ip_address': ip_address, 'board_address': board_address,
            'max_on_chip_memory_usage_for_spikes_in_bytes': (
                max_on_chip_memory_usage_for_spikes_in_bytes),
            'space_before_notification': space_before_notification,
            'constraints': constraints, 'label': label,
            'spike_recorder_buffer_size': spike_recorder_buffer_size,
            'buffer_size_before_receive': buffer_size_before_receive})

    @staticmethod
    def build_model():
        return SpikeSourceArray
