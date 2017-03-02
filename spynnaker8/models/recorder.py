import logging
import neo
import os

from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import utility_calls

logger = logging.getLogger(__name__)


class Recorder(RecordingCommon):
    def __init__(self, population):
        RecordingCommon.__init__(self, population)

    @staticmethod
    def _get_io(filename):
        """
        Return a Neo IO instance, guessing the type based on the filename
        suffix.
        """
        logger.debug("Creating Neo IO for filename %s" % filename)
        dir = os.path.dirname(filename)
        utility_calls.check_directory_exists_and_create_if_not(dir)
        extension = os.path.splitext(filename)[1]
        if extension in ('.txt', '.ras', '.v', '.gsyn'):
            raise IOError(
                "ASCII-based formats are not currently supported for output"
                " data. Try using the file extension '.pkl' or '.h5'")
        elif extension in ('.h5',):
            return neo.io.NeoHdf5IO(filename=filename)
        elif extension in ('.pkl', '.pickle'):
            return neo.io.PickleIO(filename=filename)
        elif extension == '.mat':
            return neo.io.NeoMatlabIO(filename=filename)
        else:  # function to be improved later
            raise Exception("file extension %s not supported" % extension)
