from neo import Segment


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

    @property
    def analogsignalarrays(self):
        return self._analog_signal_arrays

    @analogsignalarrays.setter
    def analogsignalarrays(self, new_value):
        self._analog_signal_arrays = new_value
