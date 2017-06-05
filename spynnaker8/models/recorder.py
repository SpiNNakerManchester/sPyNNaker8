import logging
import neo
import os
import numpy
from datetime import datetime
import quantities as pq
from collections import defaultdict

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
from spinn_front_end_common.utilities import globals_variables
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

        # create neo blocks for recording (needed due to pynn demand
        # of runs being inside the neo block
        self._previous_spikes = list()
        self._previous_v = list()
        self._previous_gsyn_exc = list()
        self._previous_gsyn_inh = list()
        self._previous_segment_data = set()
        self._runtime_to_segment_time_mapping = defaultdict(datetime.now)
        self._has_read_blocks_spikes = False
        self._has_read_blocks_v = False
        self._has_read_blocks_gsyn_exc = False
        self._has_read_blocks_gsyn_inh = False

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

    def reset_neo_recorded_trackers(self):
        """ resets recorder tracker for ease later.

        :rtype: None
        """
        self._has_read_blocks_spikes = False
        self._has_read_blocks_v = False
        self._has_read_blocks_gsyn_exc = False
        self._has_read_blocks_gsyn_inh = False

    def _extract_data(self, variables, clear, annotations):
        """ extracts data from the vertices and puts them into a neo block

        :param variables: the variables to extract
        :param clear: =if the variables should be cleared after reading
        :param annotations: annotations to put on the neo block
        :return: The neo block
        """

        # if all are needed to be extracted, extract each and plonk into the
        # neo block segment
        if variables == 'all':
            variables = self._get_all_possible_recordable_variables()

        # if variable is a base string, plonk into a array for ease of
        # conversion
        if isinstance(variables, basestring):
            variables = [variables]

        neo_block = SpynnakerNeoBlock()
        neo_block.name = self._population.label
        neo_block.description = self._population.describe()

        # iterate through variables adding to a new neo block for end user use
        self._get_data(variables, neo_block)

        # add fluff to the neo block
        neo_block.annotate(**self._metadata())
        if annotations:
            neo_block.annotate(**annotations)

        if clear:
            self._clear_recording(variables)
        return neo_block

    def _filter_recorded(self, filter_ids):
        """ create neo filter

        :param filter_ids: the ids of the pop to filter.
        :return: the filter
        """
        record_ids = list()
        for neuron_id in range(0, len(filter_ids)):
            if filter_ids[neuron_id]:
                # add population first id to ensure all atoms have a unique
                # identifier (pynn enforcement)
                record_ids.append(neuron_id + self._population._first_id)
        return record_ids

    def _get_data(self, variables, neo_block):
        """ extract data and generate neo segments as needed

        :param variables: variables to extract data from
        :param neo_block: The neo block to fill in
        :rtype: None
        """

        # insert previous data
        segment = self._insert_previous_segments(variables, neo_block)

        for variable in variables:

            if variable == "spikes":
                if not self._has_read_blocks_spikes:

                    # create new segment if needed
                    segment = self._build_segment(segment)

                    # get new spikes
                    spikes = self._get_recorded_variable('spikes')

                    # clear them from buffer manager
                    self._population._vertex.clear_spike_recording(
                        globals_variables.get_simulator().buffer_manager,
                        globals_variables.get_simulator().placements,
                        globals_variables.get_simulator().graph_mapper)

                    # store in tracker
                    self._previous_spikes.append(spikes)

                    # plonk in segment
                    self._read_in_spikes(spikes, segment)

                    # state that read in spikes for this period
                    self._has_read_blocks_spikes = True
                    neo_block.segments.append(segment)
            else:
                # filter
                ids = sorted(self._filter_recorded(
                    self._indices_to_record[variable]))
                vertex = self._population._vertex

                # check each variable
                if variable == "v":
                    if not self._has_read_blocks_v:
                        # get v
                        segment = self._get_analog_signal(
                            variable, self._get_recorded_variable,
                            vertex.clear_v_recording,
                            self._previous_v, ids, segment)
                        self._has_read_blocks_v = True
                        neo_block.segments.append(segment)

                if variable == "gsyn_exc":
                    if not self._has_read_blocks_gsyn_exc:
                        segment = self._get_analog_signal(
                            variable, self._get_recorded_variable,
                            vertex.clear_gsyn_excitatory_recording,
                            self._previous_gsyn_exc, ids, segment)
                        self._has_read_blocks_gsyn_exc = True
                        neo_block.segments.append(segment)

                if variable == "gsyn_inh":
                    if not self._has_read_blocks_gsyn_inh:
                        segment = self._get_analog_signal(
                            variable, self._get_recorded_variable,
                            vertex.clear_gsyn_inhibitory_recording,
                            self._previous_gsyn_inh, ids, segment)
                        self._has_read_blocks_gsyn_inh = True
                        neo_block.segments.append(segment)

    def _get_analog_signal(
            self, variable, record_call, clear_call, previous, ids, segment):
        """ get analog signal

        :param variable: analog signal to extract
        :param clear_call: buffer manager clean data call
        :param previous: the previous data holder
        :param ids: the filter.
        :return: the segment.
        """

        # create new segment if needed
        segment = self._build_segment(segment)

        signal_array = record_call(variable)
        clear_call(
            globals_variables.get_simulator().buffer_manager,
            globals_variables.get_simulator().placements,
            globals_variables.get_simulator().graph_mapper)
        previous.append(signal_array)
        self._read_in_signal(signal_array, segment, ids, variable)
        return segment

    def _build_segment(self, current_last_segment):
        """ builds or hands out a segment.

        :param current_last_segment: None or a Segment
        :type current_last_segment: None or SpynnakerNeoSegment
        :return: a segment
        """

        # locate current time for this segment
        time_now = self._runtime_to_segment_time_mapping[
            globals_variables.get_simulator().t]
        if (current_last_segment is None or
                (current_last_segment is not None and
                 current_last_segment.rec_datetime != time_now)):
            return self._create_segment(time_now)
        else:
            return current_last_segment

    def _create_segment(self, time_now):
        """ build segment for the current data to be gathered in store current\
          time

        :param time_now: time to put in segment
        :return: segment object
        """

        segment_counter = globals_variables.get_simulator().segment_counter

        segment = SpynnakerNeoSegment(
            name="segment{}".format(segment_counter),
            description=self._population.describe(),
            rec_datetime=time_now)

        # record this segment data for future
        self._previous_segment_data.add((time_now, segment_counter))
        self._runtime_to_segment_time_mapping[
            globals_variables.get_simulator().t] = time_now

        return segment

    def _insert_previous_segments(self, variables, neo_block):
        """ inserts data for previous segments that have been recorded

        :param variables: the variables to get data from
        :param neo_block: the neo block to put them in
        :return: the last segment which has data.
        """
        position = 0
        segment = None
        for segment_data in self._previous_segment_data:
            segment = SpynnakerNeoSegment(
                name="segment{}".format(segment_data[1]),
                description=self._population.describe(),
                rec_datetime=segment_data[0])
            wrote_data = False
            for variable in variables:
                if variable == "spikes":
                    if len(self._previous_spikes) > position:
                        wrote_data = True
                        self._read_in_spikes(
                            self._previous_spikes[position], segment)

                # filter
                ids = sorted(self._filter_recorded(
                    self._indices_to_record[variable]))

                if variable == "v":
                    if len(self._previous_v) > position:
                        wrote_data = True
                        self._read_in_signal(
                            self._previous_v[position], segment, ids, variable)
                if variable == "gsyn_exc":
                    if len(self._previous_gsyn_exc) > position:
                        wrote_data = True
                        self._read_in_signal(
                            self._previous_gsyn_exc[position], segment, ids,
                            variable)
                if variable == "gsyn_inh":
                    if len(self._previous_gsyn_inh) > position:
                        wrote_data = True
                        self._read_in_signal(
                            self._previous_gsyn_inh[position], segment, ids,
                            variable)
            position += 1

            # to support others putting data in
            if wrote_data:
                neo_block.segments.append(segment)
        return segment

    def _read_in_signal(self, signal_array, segment, ids, variable):
        """ reads in a data item that's not spikes (likely v, gsyn e, gsyn i)

        :param signal_array: the raw signal data
        :type signal_array: iterable
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
        """  converts a none spikes data into neo format

        :param signal_array: v, gsyn stuff
        :param channel_indices: filter
        :return: the neo friendly data
        """
        processed_data = [
            signal_array[:, 2][signal_array[:, 0] == index]
            for index in channel_indices]
        processed_data = numpy.vstack(processed_data).T
        return processed_data

    def _read_in_spikes(self, spikes, segment):
        """ converts numpy spikes into neo spike and adds to segment.

        :param spikes: numpy spikes
        :param segment: neo segment.
        :rtype: None
        """
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
                    source_index=self._population.id_to_index(atom_id)))

    def _get_all_possible_recordable_variables(self):
        """ generates list of all recorders

        :return: string list
        """
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
        """ metadata thingy

        :return: the metadata thingy
        """
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
        """ goes through and clears all the recordings as needed

        :param variables: variables to clean
        :rtype: None
        """
        self._previous_segment_data = list()
        self._runtime_to_segment_time_mapping = defaultdict(datetime.now)
        for variable in variables:
            if variable == 'spikes':
                self._spikes_neo_recorder = list()
            elif variable == "v":
                self._v_neo_recorder = list()
            elif variable == "gsyn_inh":
                self._gsyn_inh_neo_recorder = list()
            elif variable == "gsyn_exc":
                self._gsyn_inh_neo_recorder = list()
            else:
                raise exceptions.InvalidParameterType(
                    "The variable {} is not a recordable value".format(
                        variable))
