from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import globals_variables
from spynnaker8.utilities.data_holder import DataHolder

import numpy

from spynnaker8.utilities.id import ID


class Population(PyNNPopulationCommon, RecordingCommon):
    """ pynn 0.8 population object

    """

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 initial_values=None, label=None):

        # hard code initial values as required
        if initial_values is None:
            initial_values = {}

        if isinstance(cellclass, DataHolder):
            vertex_holder = cellclass
            vertex_holder.add_item(
                'label', self.create_label(vertex_holder.data_items['label']))
            vertex_holder.add_item('n_neurons', size)
            assert cellparams is None  # cellparams being retained for backwards compatibility, but use is deprecated
        elif issubclass(cellclass, DataHolder):
            internal_params = dict(cellparams)
            internal_params['label'] = self.create_label(label)
            internal_params['n_neurons'] = size
            vertex_holder = cellclass(**internal_params)
            # emit deprecation warning
        else:
            raise TypeError(
                "cellclass must be an instance or subclass of BaseCellType,"
                " not a %s" % type(cellclass))

        # convert between data holder and model
        vertex = vertex_holder.build_model()(**vertex_holder.data_items)

        # build our initial objects
        PyNNPopulationCommon.__init__(
            self, spinnaker_control=globals_variables.get_simulator(),
            size=size, vertex=vertex,
            structure=structure, initial_values=initial_values)
        RecordingCommon.__init__(self, population=self)

        # things for pynn demands
        self._all_ids = self.get_all_ids()
        self._first_id = self._all_ids[0]
        self._last_id = self._all_ids[-1]

    @property
    def label(self):
        return self._vertex.label

    @label.setter
    def label(self, new_value):
        self._vertex.label = new_value

    def id_to_index(self, id):
        """
        Given the ID(s) of cell(s) in the Population, return its (their) index
        (order in the Population).
        """
        if not numpy.iterable(id):
            if not self._first_id <= id <= self._last_id:
                raise ValueError(
                    "id should be in the range [{},{}], actually {}".format(
                        self._first_id, self._last_id, id))
            return int(id - self._first_id)  # this assumes ids are consecutive

    def get_all_ids(self):
        id_range = numpy.arange(
            globals_variables.get_simulator().id_counter,
            globals_variables.get_simulator().id_counter + self.size)
        return numpy.array(
            [ID(atom_id) for atom_id in id_range], dtype=ID)

    def record(self, variables, to_file=None, sampling_interval=None):
        """
        Record the specified variable or variables for all cells in the
        Population or view.

        `variables` may be either a single variable name or a list of variable
        names. For a given celltype class, `celltype.recordable` contains a
        list of variables that can be recorded for that celltype.

        If specified, `to_file` should be a Neo IO instance and `write_data()`
        will be automatically called when `end()` is called.

        `sampling_interval` should be a value in milliseconds, and an integer
        multiple of the simulation timestep.
        """
        if variables is None:  # reset the list of things to record
            # note that if record(None) is called, its a reset
            RecordingCommon._reset(self)
        else:
            for variable in variables:
                self._record(
                    variable, self._all_ids, sampling_interval, to_file)

    def _end(self):
        """ Do final steps at the end of the simulation
        """
        if self._write_to_files_indicators['spikes'] is not None:
            self.write_data
            self.printSpikes(self._record_spike_file)
        if self._write_to_files_indicators['v'] is not None:
            self.print_v(self._record_v_file)
        if self._write_to_files_indicators['gsyn_exc'] is not None:
            self.print_gsyn_exc(self._record_gsyn_file)
        if self._write_to_files_indicators['gsyn_inh'] is not None:
