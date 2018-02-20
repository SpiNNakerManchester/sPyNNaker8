import logging
import numpy

from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.utilities.constants import SPIKES
from spinn_front_end_common.utilities import exceptions
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.exceptions import ConfigurationException

from spynnaker8.models import Recorder
from spynnaker8.models.populations import IDMixin
from spynnaker8.utilities import DataHolder

from pyNN import descriptions

logger = logging.getLogger(__name__)


class Population(PyNNPopulationCommon, Recorder):
    """ pynn 0.8 population object

    """

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 initial_values=None, label=None):

        size = self._roundsize(size, label)

        # hard code initial values as required
        if initial_values is None:
            initial_values = {}

        if isinstance(cellclass, DataHolder):
            self._vertex_holder = cellclass
            self._vertex_holder.add_item(
                'label', self.create_label(
                    self._vertex_holder.data_items['label'], label))
            assert cellparams is None
        # cellparams being retained for backwards compatibility, but use
        # is deprecated
        elif issubclass(cellclass, DataHolder):
            internal_params = dict(cellparams)
            cell_label = None
            if 'label' in internal_params:
                cell_label = internal_params['label']
            internal_params['label'] = self.create_label(cell_label, label)
            self._vertex_holder = cellclass(**internal_params)
            # emit deprecation warning
        else:
            raise TypeError(
                "cellclass must be an instance or subclass of BaseCellType,"
                " not a %s" % type(cellclass))

        if 'n_neurons' in self._vertex_holder.data_items:
            if size is None:
                size = self._vertex_holder.data_items['n_neurons']
            else:
                if size != self._vertex_holder.data_items['n_neurons']:
                    raise ConfigurationException(
                        "Size parameter is {} but the {} expects a size of {}"
                        "".format(size, cellclass,
                                  self._vertex_holder.data_items['n_neurons']))
        else:
            if size is None:
                raise ConfigurationException(
                    "Size parameter can not be None for {}".format(cellclass))
            else:
                self._vertex_holder.add_item('n_neurons', size)

        # convert between data holder and model (uses ** so that its taken
        # the dictionary to be the parameters themselves)
        vertex = self._vertex_holder.build_model()(
            **self._vertex_holder.data_items)

        # build our initial objects
        PyNNPopulationCommon.__init__(
            self, spinnaker_control=globals_variables.get_simulator(),
            size=size, vertex=vertex,
            structure=structure, initial_values=initial_values)
        Recorder.__init__(self, population=self)

        # annotations used by neo objects
        self._annotations = dict()

    @property
    def annotations(self):
        """ returns annotations given by the end user

        :return:
        """
        return self._annotations

    @property
    def celltype(self):
        """
        Implements the pynn expected celltype propery
        :return: The celltype this property has been set to
        """
        return self._vertex_holder

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
            Recorder._turn_off_all_recording(self)
            # handle one element vs many elements
        elif isinstance(variables, basestring):
            # handle special case of 'all'
            if variables == "all":
                logger.warn(
                    "This is not currently standard PyNN, and therefore "
                    "may not work in other simulators.")

                # get all possible recordings for this vertex
                variables = self._get_all_possible_recordable_variables()

                # iterate though them
                for variable in variables:
                    self._record(variable, self._all_ids,
                                 sampling_interval, to_file)
            else:
                # record variable
                self._record(
                    variables, self._all_ids, sampling_interval, to_file)

        else:  # list of variables, so just iterate though them
            for variable in variables:
                self._record(
                    variable, self._all_ids, sampling_interval, to_file)

    def write_data(self, io, variables='all', gather=True, clear=False,
                   annotations=None):
        """
        Write recorded data to file, using one of the file formats supported by
        Neo.

        :param io: a Neo IO instance
        :type io: neo instance or a string for where to put a neo instance
        :param variables:
            either a single variable name or a list of variable names.
            Variables must have been previously recorded, otherwise an
            Exception will be raised.
        :type variables: string or list of string
        :param gather: pointless in spynnaker
        :param clear:
        clears the storage data if set to true after reading it back
        :param annotations: ???????????
        """

        if not gather:
            logger.warn("Spinnaker only supports gather=True. We will run as "
                        "if gather was set to True.")

        if isinstance(io, basestring):
            io = self._get_io(io)

        data = self._extract_neo_block(variables, clear, annotations)
        # write the neo block to the file
        io.write(data)

    def describe(self, template='population_default.txt', engine='default'):
        """
        Returns a human-readable description of the population.

        The output may be customized by specifying a different template
        together with an associated template engine (
        see :mod:`pyNN.descriptions`).

        If template is None, then a dictionary containing the template context
        will be returned.
        """
        vertex_context = self._vertex.describe()

        context = {
            "label": self.label,
            "celltype": vertex_context,
            "structure": None,
            "size": self.size,
            "size_local": self.size,
            "first_id": self._first_id,
            "last_id": self._last_id,
        }
        context.update(self._annotations)
        if self.size > 0:
            context.update({
                "local_first_id": self._first_id,
                "cell_parameters": {}})
        if self._structure:
            context["structure"] = self._structure.describe(template=None)
        return descriptions.render(engine, template, context)

    def _end(self):
        """ Do final steps at the end of the simulation
        """
        for variable in self._write_to_files_indicators.keys():
            if self._write_to_files_indicators[variable] is not None:
                self.write_data(
                    io=self._write_to_files_indicators[variable],
                    variables=[variable])

    def get_data(
            self, variables='all', gather=True, clear=False, annotations=None):
        """
        Return a Neo `Block` containing the data (spikes, state variables)
        recorded from the Assembly.

        `variables` - either a single variable name or a list of variable names
                      Variables must have been previously recorded,
                      otherwise an Exception will be raised.

        For parallel simulators, if `gather` is True, all data will be gathered
        to all nodes and the Neo `Block` will contain data from all nodes.
        Otherwise, the Neo `Block` will contain only data from the cells
        simulated on the local node.

        If `clear` is True, recorded data will be deleted from the `Assembly`.
        """
        if not gather:
            logger.warn("Spinnaker only supports gather=True. We will run as "
                        "if gather was set to True.")

        return self._extract_neo_block(variables, clear, annotations)

    def spinnaker_get_data(self, variable):
        """ public assessor for getting data as a numpy array, instead of
        the neo based object

        :param variable:
        either a single variable name or a list of variable names
        Variables must have been previously recorded, otherwise an
        Exception will be raised.
        :return: numpy array of the data
        """
        logger.warn(
            "This call is not standard pynn and therefore will not be "
            "compatible between simulators. Nor do we guarantee that this "
            "function will exist in future releases.")
        if isinstance(variable, list):
            if len(variable) == 1:
                variable = variable[0]
            else:
                msg = "Only one type of data at a time is supported"
                raise exceptions.ConfigurationException(msg)
        return self._get_recorded_variable(variable)

    def get_spike_counts(self, gather=True):
        """ Return the number of spikes for each neuron.
        """
        spikes = self._get_recorded_variable(SPIKES)
        return PyNNPopulationCommon.get_spike_counts(self, spikes, gather)

    def find_units(self, variable):
        """ supports getting the units of a variable

        :param variable:
        :return:
        """
        return self._get_variable_unit(variable)

    def set(self, **kwargs):
        for parameter, value in kwargs.iteritems():
            try:
                PyNNPopulationCommon.set(self, parameter, value)
            except InvalidParameterType:
                PyNNPopulationCommon.initialize(self, parameter, value)

    def initialize(self, **kwargs):
        for parameter, value in kwargs.iteritems():
            PyNNPopulationCommon.initialize(self, parameter, value)

    @property
    def initial_values(self):
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation")
        return self._vertex.initial_values

    def get(self, parameter_names, gather=False, simplify=True):
        if simplify is not True:
            logger.warn("The simplify value is ignored if not set to true")
        return PyNNPopulationCommon.get(self, parameter_names, gather)

    @property
    def all_cells(self):
        cells = []
        for id in xrange(self._size):
            cells.append(IDMixin(self, id))
        return cells

    @property
    def local_cells(self):
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "local_cells just returns all_cells")
        return self.all_cells

    @property
    def position_generator(self):
        def gen(i):
            return self.positions[:, i]
        return gen

    def is_local(self, id):
        logger.warning("local calls do not really make sense on sPyNNaker so "
                       "is_local always retruns True")
        return True
