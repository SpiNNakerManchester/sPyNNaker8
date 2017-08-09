import logging
import neo
import os
import numpy
from datetime import datetime
from spinn_utilities.ordered_set import OrderedSet

from spynnaker.pyNN.models.common import AbstractNeuronRecordable
from spynnaker.pyNN.models.common import AbstractSpikeRecordable
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import utility_calls
from spinn_front_end_common.utilities.globals_variables import get_simulator
from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker8.models.data_cache import DataCache
from spynnaker8.utilities.spynnaker8_neo_block import SpynnakerNeoBlock
from spynnaker8.utilities.spynnaker8_neo_segment import SpynnakerNeoSegment

logger = logging.getLogger(__name__)


class Recorder(RecordingCommon):
    def __init__(self, population):
        RecordingCommon.__init__(
            self, population, get_simulator().machine_time_step / 1000.0)
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

    def _extract_data(self, variables, clear, annotations):
        """ extracts data from the vertices and puts them into a neo block

        :param variables: the variables to extract
        :param clear: =if the variables should be cleared after reading
        :param annotations: annotations to put on the neo block
        :return: The neo block
        """

        data = SpynnakerNeoBlock()

        for previous in range(0, get_simulator().segment_counter):
            data.segments.append(
                self._get_previous_segment(previous, variables))

        # add to the segments the new data
        data.segments.append(self._get_current_segment(variables, clear))

        # add fluff to the neo block
        data.name = self._population.label
        data.description = self._population.describe()
        data.rec_datetime = data.segments[0].rec_datetime
        data.annotate(**self._metadata())
        if annotations:
            data.annotate(**annotations)
        return data

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
            if variable == "spikes":
                return "spikes"
            if variable == "v":
                return "mV"
            if variable == "gsyn_exc":
                return "uS"
            if variable == "gsyn_inh":
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
                t=get_simulator().t, sampling_interval=self._sampling_interval,
                first_id=self._population._first_id)

            for variable in variables:
                data = self._get_recorded_variable(variable)
                ids = sorted(
                    self._filter_recorded(self._indices_to_record[variable]))
                indexes = numpy.array(
                    [self._population.id_to_index(atom_id) for atom_id in ids])
                data_cache.save_data(
                    variable=variable, data=data, ids=ids, indexes=indexes,
                    units=self._get_units(variable))
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

    def _get_current_segment(self, variables, clear):

        # build segment for the current data to be gathered in
        segment = SpynnakerNeoSegment(
            name="segment{}".format(get_simulator().segment_counter),
            description=self._population.describe(),
            rec_datetime=datetime.now())

        # sort out variables for using
        variables = self._clean_variables(variables)

        for variable in variables:
            ids = sorted(
                self._filter_recorded(self._indices_to_record[variable]))
            indexes = numpy.array(
                [self._population.id_to_index(atom_id) for atom_id in ids])
            if variable == "spikes":
                segment.read_in_spikes(
                    spikes=self._get_recorded_variable(variable),
                    t=get_simulator().get_current_time(),
                    ids=ids, indexes=indexes,
                    first_id=self._population._first_id,
                    recording_start_time=self._recording_start_time,
                    label=self._population.label)
            else:
                segment.read_in_signal(
                    signal_array=self._get_recorded_variable(variable),
                    ids=ids, indexes=indexes, variable=variable,
                    recording_start_time=self._recording_start_time,
                    sampling_interval=self._sampling_interval,
                    units=self._get_units(variable),
                    label=self._population.label)
        if clear:
            self._clear_recording(variables)
        return segment

    def _get_previous_segment(self, segment_number, variables):
        if segment_number not in self._data_cache:
            logger.warn("No Data available for Segment {}"
                        .format(segment_number))
            segment = SpynnakerNeoSegment(
                name="segment{}".format(segment_number),
                description="Empty",
                rec_datetime=datetime.now())
            return segment

        data_cache = self._data_cache[segment_number]

        # sort out variables
        variables = self._clean_variables(variables)

        # build segment for the previous data to be gathered in
        segment = SpynnakerNeoSegment(
            name="segment{}".format(segment_number),
            description=data_cache.description,
            rec_datetime=data_cache.rec_datetime)

        for variable in variables:
            if variable not in data_cache.variables:
                logger.warn("No Data available for Segment {} variable {}"
                            "".format(segment_number, variable))
                continue
            variable_cache = data_cache.get_data(variable)
            if variable == "spikes":
                segment.read_in_spikes(
                    spikes=variable_cache.data,
                    t=data_cache.t,
                    ids=variable_cache.ids,
                    indexes=variable_cache.indexes,
                    first_id=data_cache.first_id,
                    recording_start_time=data_cache.recording_start_time,
                    label=data_cache.label)
            else:
                segment.read_in_signal(
                    signal_array=variable_cache.data,
                    ids=variable_cache.ids,
                    indexes=variable_cache.indexes,
                    variable=variable,
                    recording_start_time=data_cache.recording_start_time,
                    sampling_interval=data_cache.sampling_interval,
                    units=variable_cache.units,
                    label=data_cache.label)
        return segment

    def _get_all_possible_recordable_variables(self):
        variables = OrderedSet()
        if isinstance(self._population._vertex, AbstractSpikeRecordable):
            variables.add('spikes')
        if isinstance(self._population._vertex, AbstractNeuronRecordable):
            variables.update(
                self._population._vertex.get_recordable_variables())
        return variables

    def _get_all_recording_variables(self):
        possibles = self._get_all_possible_recordable_variables()
        variables = OrderedSet()
        for possible in possibles:
            if possible == "spikes":
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
            if variable == 'spikes':
                self._population._vertex.clear_spike_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == "v":
                self._population._vertex.clear_v_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == "gsyn_inh":
                self._population._vertex.clear_gsyn_inhibitory_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            elif variable == "gsyn_exc":
                self._population._vertex.clear_gsyn_excitatory_recording(
                    get_simulator().buffer_manager,
                    get_simulator().placements,
                    get_simulator().graph_mapper)
            else:
                raise InvalidParameterType(
                    "The variable {} is not a recordable value".format(
                        variable))
