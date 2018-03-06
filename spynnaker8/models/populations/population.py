import logging
import numpy

from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.utilities.constants import SPIKES
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.exceptions import ConfigurationException

from spynnaker8.models import Recorder
from spynnaker8.models.populations import IDMixin, PopulationBase
from spynnaker8.utilities import DataHolder

from pyNN import descriptions

logger = logging.getLogger(__name__)


class Population(PyNNPopulationCommon, Recorder, PopulationBase):
    """ PyNN 0.8/0.9 population object
    """

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 initial_values=None, label=None):
        # pylint: disable=too-many-arguments
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
            if cellparams is None:
                internal_params = dict()
            else:
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
            elif size != self._vertex_holder.data_items['n_neurons']:
                raise ConfigurationException(
                    "Size parameter is {} but the {} expects a size of {}"
                    "".format(size, cellclass,
                              self._vertex_holder.data_items['n_neurons']))
        else:
            if size is None:
                raise ConfigurationException(
                    "Size parameter can not be None for {}".format(cellclass))
            self._vertex_holder.add_item('n_neurons', size)

        # convert between data holder and model (uses ** so that its taken
        # the dictionary to be the parameters themselves)
        vertex = self._vertex_holder.build_model()(
            **self._vertex_holder.data_items)

        # build our initial objects
        super(Population, self).__init__(
            spinnaker_control=globals_variables.get_simulator(),
            size=size, vertex=vertex,
            structure=structure, initial_values=initial_values)
        Recorder.__init__(self, population=self)

        # annotations used by neo objects
        self._annotations = dict()

    def __iter__(self):
        """ Iterate over local cells
        """
        for id in xrange(self._size):
            yield IDMixin(self, id)

    def all(self):
        """ Iterator over cell ids on all MPI nodes."""
        for id in xrange(self._size):
            yield IDMixin(self, id)

    @property
    def annotations(self):
        """ The annotations given by the end user
        """
        return self._annotations

    @property
    def celltype(self):
        """ Implements the PyNN expected celltype property

        :return: The celltype this property has been set to
        """
        return self._vertex_holder

    def can_record(self, variable):
        """ Determine whether `variable` can be recorded from this population.
        """
        return variable in self._get_all_possible_recordable_variables()

    def record(self, variables, to_file=None, sampling_interval=None,
               indexes=None):
        """ Record the specified variable or variables for all cells in the\
            Population or view.

        :param variables: either a single variable name or a list of variable\
            names. For a given celltype class, `celltype.recordable` contains\
            a list of variables that can be recorded for that celltype.
        :type variables: str or list(str)
        :param to_file: a file to automatically record to (optional).\
            `write_data()` will be automatically called when `end()` is called.
        :type to_file: a Neo IO instance
        :param sampling_interval: a value in milliseconds, and an integer\
            multiple of the simulation timestep.
        """
        if indexes is not None:
            logger.warn(
                "record indexes parameter is not standard PyNN so will not "
                "work on other other simulators. "
                "In the future this will be replaced with views")
        if variables is None:  # reset the list of things to record
            # note that if record(None) is called, its a reset
            Recorder._turn_off_all_recording(self)
            # handle one element vs many elements
        elif isinstance(variables, basestring):
            # handle special case of 'all'
            if variables == "all":
                logger.warning(
                    "This is not currently standard PyNN, and therefore "
                    "may not work in other simulators.")

                # get all possible recordings for this vertex
                variables = self._get_all_possible_recordable_variables()

                # iterate though them
                for variable in variables:
                    self._record(variable, sampling_interval, to_file, indexes)
            else:
                # record variable
                self._record(variables, sampling_interval, to_file, indexes)

        else:  # list of variables, so just iterate though them
            for variable in variables:
                self._record(variable, sampling_interval, to_file, indexes)

    def write_data(self, io, variables='all', gather=True, clear=False,
                   annotations=None):
        """ Write recorded data to file, using one of the file formats\
            supported by Neo.

        :param io: \
            a Neo IO instance, or a string for where to put a neo instance
        :type io: neo instance or str
        :param variables: \
            either a single variable name or a list of variable names.\
            Variables must have been previously recorded, otherwise an\
            Exception will be raised.
        :type variables: str or list(str)
        :param gather: pointless on sPyNNaker
        :param clear: \
            clears the storage data if set to true after reading it back
        :param annotations: annotations to put on the neo block
        """
        # pylint: disable=too-many-arguments
        if not gather:
            logger.warning("Spinnaker only supports gather=True. We will run "
                           "as if gather was set to True.")

        if isinstance(io, basestring):
            io = self._get_io(io)

        data = self._extract_neo_block(variables, clear, annotations)
        # write the neo block to the file
        io.write(data)

    def describe(self, template='population_default.txt', engine='default'):
        """ Returns a human-readable description of the population.

        The output may be customized by specifying a different template\
        together with an associated template engine (see\
        :mod:`pyNN.descriptions`).

        If `template` is None, then a dictionary containing the template\
        context will be returned.
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
        for variable in self._write_to_files_indicators:
            if self._write_to_files_indicators[variable] is not None:
                self.write_data(
                    io=self._write_to_files_indicators[variable],
                    variables=[variable])

    def get_data(
            self, variables='all', gather=True, clear=False, annotations=None):
        """ Return a Neo `Block` containing the data\
            (spikes, state variables) recorded from the Assembly.

        :param variables: either a single variable name or a list of variable\
            names. Variables must have been previously recorded, otherwise an
            Exception will be raised.
        :type variables: str or list
        :param: Whether to collect data from all MPI nodes or just the current\
            node (irrelevant on sPyNNaker, which always behaves as if True)
        :type gather: bool
        :param: Whether recorded data will be deleted from the `Assembly`.
        :type clear: bool
        :param annotations: annotations to put on the neo block
        :type annotations: dict
        :rtype: neo.Block
        """
        if not gather:
            logger.warning("Spinnaker only supports gather=True. We will run "
                           "as if gather was set to True.")

        return self._extract_neo_block(variables, clear, annotations)

    def spinnaker_get_data(self, variable):
        """ Public accessor for getting data as a numpy array, instead of\
            the neo based object

        :param variable: \
            either a single variable name or a list of variable names.\
            Variables must have been previously recorded, otherwise an\
            Exception will be raised.
        :return: numpy array of the data
        """
        logger.warning(
            "This call is not standard PyNN and therefore will not be "
            "portable to other PyNN simulators. Nor do we guarantee that this "
            "function will exist in future releases.")
        if isinstance(variable, list):
            if len(variable) == 1:
                variable = variable[0]
            else:
                msg = "Only one type of data at a time is supported"
                raise ConfigurationException(msg)
        if variable == SPIKES:
            return self._get_spikes()
        return self._get_recorded_pynn7(variable)

    def get_spike_counts(self, gather=True):
        """ Return the number of spikes for each neuron.
        """
        spikes = self._get_spikes()
        return PyNNPopulationCommon.get_spike_counts(self, spikes, gather)

    def find_units(self, variable):
        """ Get the units of a variable

        :param variable: The name of the variable
        :return: The units of the variable
        """
        return self._get_variable_unit(variable)

    def set(self, **kwargs):
        for parameter, value in kwargs.iteritems():
            try:
                super(Population, self).set(parameter, value)
            except InvalidParameterType:
                super(Population, self).initialize(parameter, value)

    def initialize(self, **kwargs):
        for parameter, value in kwargs.iteritems():
            super(Population, self).initialize(parameter, value)

    @property
    def initial_values(self):
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation")
        return self._vertex.initial_values

    # NONE PYNN API CALL
    def get_initial_value(self, variable, selector=None ):
        """ See AbstractPopulationInitializable.get_initial_value"""
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation of {}".format(
                    variable))
        return self._vertex.get_initial_value(variable, selector)

    # NONE PYNN API CALL
    def set_initial_value(self, variable, value, selector=None ):
        """ See AbstractPopulationInitializable.set_initial_value"""
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation of {}".format(
                    variable))
        if globals_variables.get_not_running_simulator().has_ran \
                and not self._vertex_changeable_after_run:
            raise Exception("Population does not support changes after run")
        self._vertex.set_initial_value(variable, value, selector)

    # NONE PYNN API CALL
    def get_initial_values(self, selector=None):
        """ See AbstractPopulationInitializable.get_initial_values"""
        if not self._vertex_population_initializable:
            raise KeyError("Population does not support the initialisation")
        return self._vertex.get_initial_values(selector)

    def get(self, parameter_names, gather=False, simplify=True):
        if simplify is not True:
            logger.warning("The simplify value is ignored if not set to true")
        return super(Population, self).get(parameter_names, gather)

    @property
    def all_cells(self):
        cells = []
        for id in xrange(self._size):
            cells.append(IDMixin(self, id))
        return cells

    @property
    def position_generator(self):
        def gen(i):
            return self.positions[:, i]
        return gen

    @staticmethod
    def create(cellclass, cellparams=None, n=1):
        """
        Pass through method to the constructor defined by PyNN

        Create n cells all of the same type.

        Returns a Population object.

        :param cellclass: see Population.__init__
        :param cellparams: see Population.__init__
        :param n: see Population.__init__(size...)
        :return: A New Population
        """
        return Population(size=n, cellclass=cellclass, cellparams=cellparams)
