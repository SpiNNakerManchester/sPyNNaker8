import logging
import neo
import os
import numpy
import quantities
from datetime import datetime
from spinn_utilities.ordered_set import OrderedSet

from spynnaker.pyNN.models.common import AbstractNeuronRecordable
from spynnaker.pyNN.models.common import AbstractSpikeRecordable
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.utilities.constants import \
    SPIKES, MEMBRANE_POTENTIAL, GSYN_EXCIT, GSYN_INHIB
from spinn_front_end_common.utilities.globals_variables import get_simulator
from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker8.models.data_cache import DataCache
from spynnaker8.utilities.version_util import pynn8_syntax


logger = logging.getLogger(__name__)


class Recorder(RecordingCommon):
    def __init__(self, population):
        RecordingCommon.__init__(self, population)
        self._recording_start_time = get_simulator().t
        self._data_cache = {}

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

    def _extract_neo_block(self, variables, clear, annotations):
        """ extracts block from the vertices and puts them into a neo block

        :param variables: the variables to extract
        :param clear: =if the variables should be cleared after reading
        :param annotations: annotations to put on the neo block
        :return: The neo block
        """

        block = neo.Block()

        for previous in range(0, get_simulator().segment_counter):
            self._append_previous_segment(block, previous, variables)

        # add to the segments the new block
        self._append_current_segment(block, variables, clear)

        # add fluff to the neo block
        block.name = self._population.label
        block.description = self._population.describe()
        block.rec_datetime = block.segments[0].rec_datetime
        block.annotate(**self._metadata())
        if annotations:
            block.annotate(**annotations)
        return block

    def _get_units(self, variable):
        """
        Get units with some safety code if the population has trouble

        :param variable: name of the variable
        :type variable: str
        :return: type of the data
        :rtype: str
        """
        try:
            return self._population.find_units(variable)
        except Exception as ex:
            logger.warn("Population: {} Does not support units for {}"
                        "".format(self._population.label, variable))
            if variable == SPIKES:
                return "spikes"
            if variable == MEMBRANE_POTENTIAL:
                return "mV"
            if variable == GSYN_EXCIT:
                return "uS"
            if variable == GSYN_INHIB:
                return "uS"
            raise ex

    def cache_data(self):
        """ store data for later extraction

        :rtype: None
        """
        variables = self._get_all_recording_variables()
        if len(variables) != 0:
            segment_number = get_simulator().segment_counter
            logger.info("Caching data for segment {}".format(segment_number))

            data_cache = DataCache(
                label=self._population.label,
                description=self._population.describe(),
                segment_number=segment_number,
                recording_start_time=self._recording_start_time,
                t=get_simulator().t,
                first_id=self._population._first_id)

            for variable in variables:
                if variable == SPIKES:
                    data = self._get_spikes()
                    sampling_interval = self._population._vertex. \
                        get_spikes_sampling_interval()
                    ids = sorted(self._filter_recorded(
                        self._indices_to_record[variable]))
                    indexes = map(self._population.id_to_index, ids)
                else:
                    results = self._get_recorded_matrix(variable)
                    (data, indexes, sampling_interval) = results
                data_cache.save_data(
                    variable=variable, data=data, indexes=indexes,
                    units=self._get_units(variable),
                    sampling_interval=sampling_interval)
            self._data_cache[segment_number] = data_cache

    def _filter_recorded(self, filter_ids):
        record_ids = list()
        for neuron_id in range(0, len(filter_ids)):
            if filter_ids[neuron_id]:
                # add population first id to ensure all atoms have a unique
                # identifier (pynn enforcement)
                record_ids.append(neuron_id + self._population._first_id)
        return record_ids

    def _clean_variables(self, variables):
        """ sorts out variables for processing usage

        :param variables: list of variables names, or all, or single.
        :return: ordered set of variables strings.
        """
        # if variable is a base string, plonk into a array for ease of
        # conversion
        if isinstance(variables, basestring):
            variables = [variables]

        # if all are needed to be extracted, extract each and plonk into the
        # neo block segment. ensures whatever was in variables stays in
        # variables, regardless of all
        if 'all' in variables:
            variables = OrderedSet(variables)
            variables.remove('all')
            variables.update(self._get_all_recording_variables())
        return variables

    def _append_current_segment(self, block, variables, clear):

        # build segment for the current data to be gathered in
        segment = neo.Segment(
            name="segment{}".format(get_simulator().segment_counter),
            description=self._population.describe(),
            rec_datetime=datetime.now())

        # sort out variables for using
        variables = self._clean_variables(variables)

        for variable in variables:
            if variable == SPIKES:
                ids = sorted(
                    self._filter_recorded(self._indices_to_record[variable]))
                indexes = map(self._population.id_to_index, ids)
                sampling_interval = self._population._vertex. \
                    get_spikes_sampling_interval()
                read_in_spikes(
                    segment=segment,
                    spikes=self._get_spikes(),
                    t=get_simulator().get_current_time(),
                    ids=ids, indexes=indexes,
                    first_id=self._population._first_id,
                    recording_start_time=self._recording_start_time,
                    sampling_interval=sampling_interval,
                    label=self._population.label)
            else:
                (data, indexes, sampling_interval) = self._get_recorded_matrix(
                    variable)
                ids = map(self._population.index_to_id, indexes)
                read_in_signal(
                    segment=segment,
                    block=block,
                    signal_array=data,
                    ids=ids, indexes=indexes,
                    variable=variable,
                    recording_start_time=self._recording_start_time,
                    sampling_interval=sampling_interval,
                    units=self._get_units(variable),
                    label=self._population.label)

        block.segments.append(segment)

        if clear:
            self._clear_recording(variables)

    def _append_previous_segment(self, block, segment_number, variables):
        if segment_number not in self._data_cache:
            logger.warn("No Data available for Segment {}"
                        .format(segment_number))
            segment = neo.Segment(
                name="segment{}".format(segment_number),
                description="Empty",
                rec_datetime=datetime.now())
            return segment

        data_cache = self._data_cache[segment_number]

        # sort out variables
        variables = self._clean_variables(variables)

        # build segment for the previous data to be gathered in
        segment = neo.Segment(
            name="segment{}".format(segment_number),
            description=data_cache.description,
            rec_datetime=data_cache.rec_datetime)

        for variable in variables:
            if variable not in data_cache.variables:
                logger.warn("No Data available for Segment {} variable {}"
                            "".format(segment_number, variable))
                continue
            variable_cache = data_cache.get_data(variable)
            indexes = variable_cache.indexes
            ids = map(self._population.index_to_id, indexes)
            if variable == SPIKES:
                read_in_spikes(
                    segment=segment,
                    spikes=variable_cache.data,
                    t=data_cache.t,
                    ids=ids,
                    indexes=indexes,
                    first_id=data_cache.first_id,
                    recording_start_time=data_cache.recording_start_time,
                    sampling_interval=variable_cache.sampling_interval,
                    label=data_cache.label)
            else:
                read_in_signal(
                    segment=segment,
                    block=block,
                    signal_array=variable_cache.data,
                    ids=ids,
                    indexes=indexes,
                    variable=variable,
                    recording_start_time=data_cache.recording_start_time,
                    sampling_interval=variable_cache.sampling_interval,
                    units=variable_cache.units,
                    label=data_cache.label)

        block.segments.append(segment)

    def _get_all_possible_recordable_variables(self):
        variables = OrderedSet()
        if isinstance(self._population._vertex, AbstractSpikeRecordable):
            variables.add(SPIKES)
        if isinstance(self._population._vertex, AbstractNeuronRecordable):
            variables.update(
                self._population._vertex.get_recordable_variables())
        return variables

    def _get_all_recording_variables(self):
        possibles = self._get_all_possible_recordable_variables()
        variables = OrderedSet()
        for possible in possibles:
            if possible == SPIKES:
                if isinstance(self._population._vertex,
                              AbstractSpikeRecordable) \
                        and self._population._vertex.is_recording_spikes():
                    variables.add(possible)
            elif isinstance(self._population._vertex,
                            AbstractNeuronRecordable) and \
                    self._population._vertex.is_recording(possible):
                variables.add(possible)
        return variables

    def _metadata(self):
        metadata = {
            'size': self._population.size,
            'first_index': 0,
            'last_index': self._population.size,
            'first_id': int(self._population._first_id),
            'last_id': int(self._population._last_id),
            'label': self._population.label,
            'simulator': get_simulator().name,
        }
        metadata.update(self._population._annotations)
        metadata['dt'] = get_simulator().dt
        metadata['mpi_processes'] = get_simulator().num_processes
        return metadata

    def _clear_recording(self, variables):
        for variable in variables:
            if variable == SPIKES:
                self._population._vertex.clear_spike_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == MEMBRANE_POTENTIAL:
                self._population._vertex.clear_v_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == GSYN_EXCIT:
                self._population._vertex.clear_gsyn_inhibitory_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == GSYN_INHIB:
                self._population._vertex.clear_gsyn_excitatory_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            else:
                raise InvalidParameterType(
                    "The variable {} is not a recordable value".format(
                        variable))

# These functions are neo utilities.
# The only reason the are listed here is that this is currently the only use


def read_in_spikes(segment, spikes, t, ids, indexes, first_id,
                   recording_start_time, sampling_interval, label):
    """
    Converts the data into SpikeTrains and saves them to the segment

    :param segment: Segment to add spikes to
    :type segment: neo.Segment
    :param spikes: Spike data in raw spynnaker format
    :type spikes: nparray
    :param t: last simulation time
    :type t: int
    :param ids: list of the ids to save spikes for
    :type ids: nparray
    :param indexes: list of the channel indexes
    :type indexes: nparray
    :param first_id: id of first neuron
    :type first_id: int
    :param recording_start_time: time recording started
    :type  recording_start_time: int
    :param sampling_interval: how often a neuron is recorded
    :param label: recording elements label
    :type label: str
    :rtype None
    """
    t_stop = t * quantities.ms

    for (id, index) in zip(ids, indexes):
        spiketrain = neo.SpikeTrain(
            times=spikes[spikes[:, 0] == id - first_id][:, 1],
            t_start=recording_start_time,
            t_stop=t_stop,
            units='ms',
            sampling_rate=sampling_interval,
            source_population=label,
            source_id=id,
            source_index=index)
        # get times per atom
        segment.spiketrains.append(spiketrain)


def _get_channel_index(ids, block):
    # Note this code is only called if not pynn8_syntax
    for channel_index in block.channel_indexes:
        if numpy.array_equal(channel_index.index, ids):
            return channel_index
    count = len(block.channel_indexes)
    channel_index = neo.ChannelIndex(
        name="Index {}".format(count), index=ids)
    block.channel_indexes.append(channel_index)
    return channel_index


def _convert_extracted_data_into_neo_expected_format(
        signal_array, indexes):
    """
    Converts data between spynnaker format and neo format
    :param signal_array: Draw data in spynnaker format
    :type signal_array: nparray
    :rtype nparray
    """
    processed_data = [
        signal_array[:, 2][signal_array[:, 0] == index]
        for index in indexes]
    processed_data = numpy.vstack(processed_data).T
    return processed_data


def read_in_signal(segment, block, signal_array, ids, indexes, variable,
                   recording_start_time, sampling_interval, units, label):
    """ reads in a data item that's not spikes (likely v, gsyn e, gsyn i)

    Saves this data to the segment.

    :param segment: Segment to add data to
    :type segment: neo.Segment
    :param signal_array: the raw signal data
    :param segment: the segment to put the data into
    :param ids: the recorded ids
    :param variable: the variable name
    :param block: neo block
    :param indexes: the channel index's
    :param recording_start_time: when recording started
    :param sampling_interval: how often a neuron is recorded
    :param units: the units of the recorded value
    :param label: human readable label

    :return: None
    """
    t_start = recording_start_time * quantities.ms
    sampling_period = sampling_interval * quantities.ms
    if signal_array.size > 0:
        # source_ids = numpy.fromiter(ids, dtype=int)
        if pynn8_syntax:
            data_array = neo.AnalogSignalArray(
                    signal_array,
                    units=units,
                    t_start=t_start,
                    sampling_period=sampling_period,
                    name=variable,
                    source_population=label,
                    channel_index=indexes,
                    source_ids=ids)
            data_array.shape = (data_array.shape[0], data_array.shape[1])
            segment.analogsignalarrays.append(data_array)

        else:
            data_array = neo.AnalogSignal(
                signal_array,
                units=units,
                t_start=t_start,
                sampling_period=sampling_period,
                name=variable,
                source_population=label,
                source_ids=ids)
            channel_index = _get_channel_index(indexes, block)
            data_array.channel_index = channel_index
            data_array.shape = (data_array.shape[0], data_array.shape[1])
            segment.analogsignals.append(data_array)
            channel_index.analogsignals.append(data_array)
