from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import globals_variables
from spynnaker8.utilities.data_holder import DataHolder


class Population(PyNNPopulationCommon, RecordingCommon):
    """ pynn 0.8 population object

    """

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 initial_values=None, label=None):

        # hard code initial values as required
        if initial_values is None:
            initial_values = {}

        vertex_holder = None

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

    @property
    def label(self):
        return self._vertex.label

    @label.setter
    def label(self, new_value):
        self._vertex.label = new_value

    def record(self, variable, new_ids, sampling_interval=None):
        RecordingCommon._record(self, variable, new_ids, sampling_interval)
        self._population.requires_mapping(True)
