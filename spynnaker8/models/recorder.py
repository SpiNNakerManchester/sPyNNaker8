import logging
import neo
import os
import numpy
from datetime import datetime
import quantities as pq

from spynnaker.pyNN.models.common.abstract_gsyn_excitatory_recordable import \
    AbstractGSynExcitatoryRecordable
from spynnaker.pyNN.models.common.abstract_gsyn_inhibitory_recordable import \
    AbstractGSynInhibitoryRecordable
from spynnaker.pyNN.models.common.abstract_spike_recordable import \
    AbstractSpikeRecordable
from spynnaker.pyNN.models.common.abstract_v_recordable import \
    AbstractVRecordable
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.utilities import globals_variables
from spynnaker.pyNN import exceptions
from spynnaker8.utilities.spynnaker8_neo_block import SpynnakerNeoBlock
from spynnaker8.utilities.spynnaker8_neo_segment import SpynnakerNeoSegment

logger = logging.getLogger(__name__)


class Recorder(RecordingCommon):
    def __init__(self, population):
        RecordingCommon.__init__(
            self, population,
            globals_variables.get_simulator().machine_time_step / 1000.0)
        self._recording_start_time = globals_variables.get_simulator().t

    @staticmethod
    def _get_io(filename):
        """
        Return a Neo IO instance, guessing the type based on the filename
        suffix.
        """
        logger.debug("Creating Neo IO for filename %s" % filename)
        directory = os.path.dirname(filename)
        utility_calls.check_directory_exists_and_create_if_not(directory)
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

    def _extract_data(self, variables, clear, annotations):
        """ extracts data from the vertices and puts them into a neo block

        :param variables: the variables to extract
        :param clear: =if the variables should be cleared after reading
        :param annotations: annotations to put on the neo block
        :return: The neo block
        """

        data = SpynnakerNeoBlock()

        # use really bad python because pynn expects it to be there.
        # add to the segments the new data
        data.segments.append(self._get_data(variables, clear))

        # add fluff to the neo block
        data.name = self._population.label
        data.description = self._population.describe()
        data.rec_datetime = data.segments[0].rec_datetime
        data.annotate(**self._metadata())
        if annotations:
            data.annotate(**annotations)
        return data

    def _filter_recorded(self, filter_ids):
        record_ids = list()
        for neuron_id in range(0, len(filter_ids)):
            if filter_ids[neuron_id]:
                # add population first id to ensure all atoms have a unique
                # identifier (pynn enforcement)
                record_ids.append(neuron_id + self._population._first_id)
        return record_ids

    def _get_data(self, variables, clear):

        # build segment for the current data to be gathered in
        segment = SpynnakerNeoSegment(
            name="segment{}".format(
                globals_variables.get_simulator().segment_counter),
            description=self._population.describe(),
            rec_datetime=datetime.now())

        # if all are needed to be extracted, extract each and plonk into the
        # neo block segment
        if variables == 'all':
            variables = self._get_all_possible_recordable_variables()

        # if variable is a base string, plonk into a array for ease of
        # conversion
        if isinstance(variables, basestring):
            variables = [variables]

        for variable in variables:
            if variable == "spikes":
                spikes = self._get_recorded_variable('spikes')
                self._read_in_spikes(spikes, segment)
            else:
                ids = sorted(self._filter_recorded(
                    self._indices_to_record[variable]))
                signal_array = self._get_recorded_variable(variable)
                self._read_in_signal(signal_array, segment, ids, variable)
        if clear:
            self._clear_recording(variables)
        return segment

    def _read_in_signal(self, signal_array, segment, ids, variable):
        """ reads in a data item that's not spikes (likely v, gsyn e, gsyn i)

        :param signal_array: the raw signal data
        :param segment: the segment to put the data into
        :param ids: the recorded ids
        :param variable: the variable name
        :return: None
        """
        t_start = self._recording_start_time * pq.ms
        sampling_period = self._sampling_interval * pq.ms
        if signal_array.size > 0:
            channel_indices = numpy.array(
                [self._population.id_to_index(atom_id)
                 for atom_id in ids])
            processed_data = \
                self._convert_extracted_data_into_neo_expected_format(
                    signal_array, channel_indices)
            units = self._population.find_units(variable)
            source_ids = numpy.fromiter(ids, dtype=int)
            data_array = neo.AnalogSignalArray(
                    processed_data,
                    units=units,
                    t_start=t_start,
                    sampling_period=sampling_period,
                    name=variable,
                    source_population=self._population.label,
                    channel_index=channel_indices,
                    source_ids=source_ids)
            data_array.shape = (
                data_array.shape[0], data_array.shape[1])
            segment.analogsignalarrays.append(data_array)


    @staticmethod
    def _convert_extracted_data_into_neo_expected_format(
            signal_array, channel_indices):
        processed_data = [
            signal_array[:, 2][signal_array[:, 0] == index]
            for index in channel_indices]
        processed_data = numpy.vstack(processed_data).T
        return processed_data

    def _read_in_spikes(self, spikes, segment):
        t_stop = globals_variables.get_simulator().t * pq.ms

        for atom_id in sorted(self._filter_recorded(
                self._indices_to_record['spikes'])):
            # get times per atom
            segment.spiketrains.append(
                neo.SpikeTrain(
                    times=spikes[spikes[:, 0] ==
                                 atom_id - self._population._first_id][:, 1],
                    t_start=self._recording_start_time,
                    t_stop=t_stop,
                    units='ms',
                    source_population=self._population.label,
                    source_id=int(atom_id),
                    source_index=
                    self._population.id_to_index(atom_id)))

    def _get_all_possible_recordable_variables(self):
        variables = list()
        if isinstance(self._population._vertex, AbstractSpikeRecordable):
            variables.append('spikes')
        if isinstance(self._population._vertex, AbstractVRecordable):
            variables.append('v')
        if isinstance(
                self._population._vertex, AbstractGSynExcitatoryRecordable):
            variables.append('gsyn_exc')
        if isinstance(
                self._population._vertex, AbstractGSynInhibitoryRecordable):
            variables.append('gsyn_inh')
        return variables

    def _metadata(self):
        metadata = {
            'size': self._population.size,
            'first_index': 0,
            'last_index': self._population.size,
            'first_id': int(self._population._first_id),
            'last_id': int(self._population._last_id),
            'label': self._population.label,
            'simulator': globals_variables.get_simulator().name,
        }
        metadata.update(self._population._annotations)
        metadata['dt'] = globals_variables.get_simulator().dt
        metadata['mpi_processes'] = \
            globals_variables.get_simulator().num_processes
        return metadata

    def _clear_recording(self, variables):
        for variable in variables:
            if variable == 'spikes':
                self._population._vertex.clear_spike_recording(
                    globals_variables.get_simulator().buffer_manager,
                    globals_variables.get_simulator().placements,
                    globals_variables.get_simulator().graph_mapper)
            elif variable == "v":
                self._population._vertex.clear_v_recording(
                    globals_variables.get_simulator().buffer_manager,
                    globals_variables.get_simulator().placements,
                    globals_variables.get_simulator().graph_mapper)
            elif variable == "gsyn_inh":
                self._population._vertex.clear_gsyn_inhibitory_recording(
                    globals_variables.get_simulator().buffer_manager,
                    globals_variables.get_simulator().placements,
                    globals_variables.get_simulator().graph_mapper)
            elif variable == "gsyn_exc":
                self._population._vertex.clear_gsyn_excitatory_recording(
                    globals_variables.get_simulator().buffer_manager,
                    globals_variables.get_simulator().placements,
                    globals_variables.get_simulator().graph_mapper)
            else:
                raise exceptions.InvalidParameterType(
                    "The variable {} is not a recordable value".format(
                        variable))
