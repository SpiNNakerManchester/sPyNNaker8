from pyNN import recording as pynn_recording

from spynnaker.pyNN.models.recording_common import RecordingCommon

from spynnaker8.utilities import globals_variables

import logging
import numpy

logger = logging.getLogger(__name__)


class Recorder(pynn_recording.Recorder, RecordingCommon):
    """ pynn 0.8 recorder

    """

    def __init__(self, population, output_file=None):

        # create common inheritance
        RecordingCommon.__init__(
            self, population, globals_variables.get_simulator())

        # create pynn inheritance
        pynn_recording.Recorder.__init__(self, population, output_file)

    def _get_spiketimes(self, id):
        """ pynn enforced method, returns the spike times as a array of
        neuron id to list of spike times

        :param id: the id object which contains a filter
        :return: the spike times as a array of
        neuron id to list of spike times
        """
        spike_times = self._population._vertex.get_spikes()

        # Convert id to index
        index = self.population.id_to_index(id)

        # Return the numpy array of spike times associated with this index
        return spike_times[index]

    def _get_all_signals(self, variable, ids, clear):
        """ pynn enforced function. gets all the signals of a variable


        :param variable: the variable to read the signals from
        :param ids: the filter of atoms to read from
        :param clear: clears the recorded data so that its  not presented the
        next time get is called
        :return: the signals which is the recorded values.
        """

        # Stack together signals for this variable from all ids
        signal = self._population._vertex._get_recorded_variable(variable)

        # if told to clear, clear the recorded data
        if clear:
            self._population._vertex.clear_recorded_variable(variable)

        # return filtered data as a numpy array
        return numpy.vstack(
            (signal[self.population.id_to_index(atom)] for atom in ids)).T

    def _local_count(self, variable, filter_ids):
        """ enforced by pynn. Have absolutely no idea what this is for.

        :param variable: the variable to read from????
        :param filter_ids: the filtered ids to read?
        :return: the count of the spikes times????
        """

        N = {}
        if variable == 'spikes':
            for atom_id in self.filter_recorded(variable, filter_ids):
                N[int(atom_id)] = atom_id._cell.spike_times.size()
        else:
            raise Exception("Only implemented for spikes")
        return N

    @property
    def _simulator(self):
        """ forced upon us from pynn. encapsulated so that we can share
        functionality for recording common

        :return: the spinnaker control class
        """

        return self._spinnaker_control

    def record(self, variable, new_ids, sampling_interval=None):
        RecordingCommon._record(self, variable, new_ids, sampling_interval)
        self._population.requires_mapping(True)
