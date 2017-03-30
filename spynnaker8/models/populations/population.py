import numpy
import logging

from pacman.model.decorators.overrides import overrides
from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.utilities import globals_variables

from spynnaker8.models.recorder import Recorder
from spynnaker8.utilities.data_holder import DataHolder
from spynnaker8.utilities.id import ID

from pyNN import descriptions

logger = logging.getLogger(__name__)


class Population(PyNNPopulationCommon, Recorder):
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
                'label', self.create_label(
                    vertex_holder.data_items['label'], label))
            vertex_holder.add_item('n_neurons', size)
            assert cellparams is None
        # cellparams being retained for backwards compatibility, but use
        # is deprecated
        elif issubclass(cellclass, DataHolder):
            internal_params = dict(cellparams)
            cell_label = None
            if 'label' in internal_params:
                cell_label = internal_params['label']
            internal_params['label'] = self.create_label(cell_label, label)
            internal_params['n_neurons'] = size
            vertex_holder = cellclass(**internal_params)
            # emit deprecation warning
        else:
            raise TypeError(
                "cellclass must be an instance or subclass of BaseCellType,"
                " not a %s" % type(cellclass))

        # convert between data holder and model (uses ** so that its taken
        # the dictionary to be the parameters themselves)
        vertex = vertex_holder.build_model()(**vertex_holder.data_items)

        # build our initial objects
        PyNNPopulationCommon.__init__(
            self, spinnaker_control=globals_variables.get_simulator(),
            size=size, vertex=vertex,
            structure=structure, initial_values=initial_values)
        Recorder.__init__(self, population=self)

        # things for pynn demands
        self._all_ids = self._get_all_ids()
        self._first_id = self._all_ids[0]
        self._last_id = self._all_ids[-1]

        # update the simulators id_counter for giving a unique id for every
        # atom
        globals_variables.get_simulator().id_counter += size

        # annotations used by neo objects
        self._annotations = dict()

    @property
    def annotations(self):
        """ returns annotations given by the end user

        :return:
        """
        return self._annotations

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

    def _get_all_ids(self):
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
            Recorder._reset(self)
        else:
            # handle one element vs many elements
            if isinstance(variables, basestring):

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

        data = self._extract_data(variables, clear, annotations)
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
            "celltype": descriptions.render(
                engine, 'modeltype_default.txt', vertex_context),
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
                      Variables must have been previously recorded, otherwise an
                      Exception will be raised.

        For parallel simulators, if `gather` is True, all data will be gathered
        to all nodes and the Neo `Block` will contain data from all nodes.
        Otherwise, the Neo `Block` will contain only data from the cells
        simulated on the local node.

        If `clear` is True, recorded data will be deleted from the `Assembly`.
        """
        if not gather:
            logger.warn("Spinnaker only supports gather=True. We will run as "
                        "if gather was set to True.")

        return self._extract_data(variables, clear, annotations)

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
        return self._get_recorded_variable(variable)

    def find_units(self, variable):
        """ supports getting the units of a variable

        :param variable:
        :return:
        """
        return self._get_variable_unit(variable)

    @overrides(PyNNPopulationCommon.set)
    def set(self, parameter, value=None):
        try:
            PyNNPopulationCommon.set(self, parameter, value)
        except InvalidParameterType:
            self.initialize(parameter, value)

    def get(self, parameter_names, gather=False, simplify=True):
        if simplify is not True:
            logger.warn("The simplify value is ignored if not set to true")
        return PyNNPopulationCommon.get(self, parameter_names, gather)

