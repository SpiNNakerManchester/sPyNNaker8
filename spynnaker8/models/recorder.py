from pyNN import recording as pynn_recording
from spynnaker.pyNN.models.recoridng_common import RecordingCommon
from spynnaker8.utilities import globals_variables

import logging

logger = logging.getLogger(__name__)


class Recorder(pynn_recording.Recorder, RecordingCommon):
    def __init__(self, population, file=None):
        self._simulator = globals_variables.get_simulator()

        # create pynn inheritance
        pynn_recording.Recorder.__init__(self, population, file)

        # create common inheritance
        RecordingCommon.__init__(self, population._vertex)

    @property
    def sampling_interval(self):
        """ forced by the public nature of pynn variables

        :return:
        """

        return self._sampling_interval

    @sampling_interval.setter
    def sampling_interval(self, new_value):
        """ forced by the public nature of pynn variables

        :param new_value: new value for the sampling_interval
        :return: None
        """
        self._sampling_interval = new_value
