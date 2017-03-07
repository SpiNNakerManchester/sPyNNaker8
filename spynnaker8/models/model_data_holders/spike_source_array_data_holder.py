from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.spike_source.spike_source_array \
    import SpikeSourceArray
from spynnaker.pyNN.utilities import constants


class SpikeSourceArrayDataHolder(DataHolder):
    def __init__(
            self, spike_times=None, port=None, tag=None, ip_address=None,
            board_address=None,
            max_on_chip_memory_usage_for_spikes_in_bytes=(
                    constants.SPIKE_BUFFER_SIZE_BUFFERING_IN),
            space_before_notification=640, constraints=None,
            label="SpikeSourceArray",
            spike_recorder_buffer_size=(
                    constants.EIEIO_SPIKE_BUFFER_SIZE_BUFFERING_OUT),
            buffer_size_before_receive=(
                    constants.EIEIO_BUFFER_SIZE_BEFORE_RECEIVE)):
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
