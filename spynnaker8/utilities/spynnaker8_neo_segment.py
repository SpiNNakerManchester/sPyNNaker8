from neo import Segment, SpikeTrain, AnalogSignalArray
import numpy
import quantities as pq


class SpynnakerNeoSegment(Segment):
    """ spynnaker version of the neo segment holding the data elements as
    needed

    """

    def __init__(
            self, name=None, description=None, file_origin=None,
            file_datetime=None, rec_datetime=None, index=None,
            **annotations):
        Segment.__init__(self, name, description, file_origin, file_datetime,
                         rec_datetime, index, **annotations)
        self._spike_trains = list()
        self._analog_signal_arrays = list()

    @property
    def spiketrains(self):
        return self._spike_trains

    @spiketrains.setter
    def spiketrains(self, new_value):
        self._spike_trains = new_value

    def read_in_spikes(self, spikes, t, ids, indexes, first_id,
                       recording_start_time, label):
        """
        Converts the data into SpikeTrains and saves them to the segment

        :param spikes: Spike data in raw spynakker format
        :type spikes: nparray
        :param t: last simulation time
        :type t: int
        :param ids: list of the ids to save spikes for
        :type ids: nparray
        :param indexes: list of the channle indexes
        :type indexes: nparray
        :param first_id: id of first neuron
        :type first_id: int
        :param recording_start_time: time recording started
        :type  recording_start_time: int
        :param label: rocing elements label
        :type label: str
        :rtype None
        """
        t_stop = t * pq.ms

        for (id, index) in zip(ids, indexes):
            # get times per atom
            self.spiketrains.append(
                SpikeTrain(
                    times=spikes[spikes[:, 0] ==
                                 id - first_id][:, 1],
                    t_start=recording_start_time,
                    t_stop=t_stop,
                    units='ms',
                    source_population=label,
                    source_id=id,
                    source_index=index))

    @staticmethod
    def _convert_extracted_data_into_neo_expected_format(
            signal_array, channel_indices):
        """
        Converts data between spynakker format and neo format
        :param signal_array: Draw data in spynakker format
        :type signal_array: nparray
        :param channel_indices: indexes to each neuron
        :type channel_indices: nparray
        :rtype nparray
        """
        processed_data = [
            signal_array[:, 2][signal_array[:, 0] == index]
            for index in channel_indices]
        processed_data = numpy.vstack(processed_data).T
        return processed_data

    def read_in_signal(self, signal_array, ids, indexes, variable,
                       recording_start_time, sampling_interval, units, label):
        """ reads in a data item that's not spikes (likely v, gsyn e, gsyn i)

        Saves this data to the segment.

        :param signal_array: the raw signal data
        :param segment: the segment to put the data into
        :param ids: the recorded ids
        :param variable: the variable name
        :return: None
        """
        t_start = recording_start_time * pq.ms
        sampling_period = sampling_interval * pq.ms
        if signal_array.size > 0:
            processed_data = \
                self._convert_extracted_data_into_neo_expected_format(
                    signal_array, indexes)
            source_ids = numpy.fromiter(ids, dtype=int)
            data_array = AnalogSignalArray(
                    processed_data,
                    units=units,
                    t_start=t_start,
                    sampling_period=sampling_period,
                    name=variable,
                    source_population=label,
                    channel_index=indexes,
                    source_ids=source_ids)
            data_array.shape = (
                data_array.shape[0], data_array.shape[1])
            self.analogsignalarrays.append(data_array)

    @property
    def analogsignalarrays(self):
        return self._analog_signal_arrays

    @analogsignalarrays.setter
    def analogsignalarrays(self, new_value):
        self._analog_signal_arrays = new_value
