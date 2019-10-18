# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import numpy
import neo
import inspect
from six import iteritems, string_types
from pyNN import descriptions
from pyNN.random import NumpyRNG
import spinn_utilities.logger_utils as logger_utils
from pacman.model.constraints import AbstractConstraint
from pacman.model.constraints.placer_constraints import ChipAndCoreConstraint
from pacman.model.constraints.partitioner_constraints import (
    MaxVertexAtomsConstraint)
from pacman.model.graphs.application.application_vertex import (
    ApplicationVertex)
from spinn_front_end_common.utilities import globals_variables
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spynnaker.pyNN.exceptions import InvalidParameterType
from spynnaker.pyNN.models.abstract_pynn_model import AbstractPyNNModel
from spynnaker.pyNN.models.abstract_models import (
    AbstractReadParametersBeforeSet, AbstractContainsUnits,
    AbstractPopulationInitializable, AbstractPopulationSettable)
from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spinn_front_end_common.abstract_models import AbstractChangableAfterRun
from spynnaker.pyNN.utilities.constants import SPIKES
from .idmixin import IDMixin
from .population_base import PopulationBase
from .population_view import PopulationView
from spynnaker8.models.recorder import Recorder

logger = logging.getLogger(__name__)


class Population(PyNNPopulationCommon, Recorder, PopulationBase):
    """ PyNN 0.8/0.9 population object
    """
    __slots__ = [
        "_all_ids",
        "__change_requires_mapping",
        "__delay_vertex",
        "__first_id",
        "__has_read_neuron_parameters_this_run",
        "__last_id",
        "_positions",
        "__record_gsyn_file",
        "__record_spike_file",
        "__record_v_file",
        "_size",
        "__spinnaker_control",
        "__structure",
        "__vertex",
        "_vertex_changeable_after_run",
        "_vertex_contains_units",
        "_vertex_population_initializable",
        "_vertex_population_settable",
        "_vertex_read_parameters_before_set"]

    def __init__(
            self, size, cellclass, cellparams=None, structure=None,
            initial_values=None, label=None, constraints=None,
            additional_parameters=None):
        # pylint: disable=too-many-arguments

        # hard code initial values as required
        if initial_values is None:
            initial_values = {}

        model = cellclass
        if inspect.isclass(cellclass):
            if cellparams is None:
                model = cellclass()
            else:
                model = cellclass(**cellparams)
        else:
            if cellparams:
                raise ConfigurationException(
                    "cellclass is an instance which includes params so "
                    "cellparams must be None")

        self._celltype = model

        # annotations used by neo objects
        self._annotations = dict()

        # Use a provided model to create a vertex
        if isinstance(model, AbstractPyNNModel):
            if size is not None and size <= 0:
                raise ConfigurationException(
                    "A population cannot have a negative or zero size.")
            population_parameters = dict(model.default_population_parameters)
            if additional_parameters is not None:
                population_parameters.update(additional_parameters)
            self.__vertex = model.create_vertex(
                size, label, constraints, **population_parameters)

        # Use a provided application vertex directly
        elif isinstance(model, ApplicationVertex):
            if additional_parameters is not None:
                raise ConfigurationException(
                    "Cannot accept additional parameters {} when the cell is"
                    " a vertex".format(additional_parameters))
            self.__vertex = model
            if size is None:
                size = self.__vertex.n_atoms
            elif size != self.__vertex.n_atoms:
                raise ConfigurationException(
                    "Vertex size does not match Population size")
            if label is not None:
                self.__vertex.set_label(label)
            if constraints is not None:
                self.__vertex.add_constraints(constraints)

        # Fail on anything else
        else:
            raise ConfigurationException(
                "Model must be either an AbstractPyNNModel or an"
                " ApplicationVertex")

        # Introspect properties of the vertex
        self._vertex_population_settable = \
            isinstance(self.__vertex, AbstractPopulationSettable)
        self._vertex_population_initializable = \
            isinstance(self.__vertex, AbstractPopulationInitializable)
        self._vertex_changeable_after_run = \
            isinstance(self.__vertex, AbstractChangableAfterRun)
        self._vertex_read_parameters_before_set = \
            isinstance(self.__vertex, AbstractReadParametersBeforeSet)
        self._vertex_contains_units = \
            isinstance(self.__vertex, AbstractContainsUnits)

        self.__spinnaker_control = globals_variables.get_simulator()
        self.__delay_vertex = None

        # Internal structure now supported 23 November 2014 ADR
        # structure should be a valid Space.py structure type.
        # generation of positions is deferred until needed.
        self.__structure = structure
        self._positions = None

        # add objects to the SpiNNaker control class
        self.__spinnaker_control.add_population(self)
        self.__spinnaker_control.add_application_vertex(
            self.__vertex, "Population ")

        # initialise common stuff
        self._size = size
        self.__record_spike_file = None
        self.__record_v_file = None
        self.__record_gsyn_file = None

        # parameter
        self.__change_requires_mapping = True
        self.__has_read_neuron_parameters_this_run = False

        # things for pynn demands
        self._all_ids = numpy.arange(
            globals_variables.get_simulator().id_counter,
            globals_variables.get_simulator().id_counter + size)
        self.__first_id = self._all_ids[0]
        self.__last_id = self._all_ids[-1]

        # update the simulators id_counter for giving a unique ID for every
        # atom
        globals_variables.get_simulator().id_counter += size

        # set up initial values if given
        if initial_values is not None:
            for variable, value in iteritems(initial_values):
                self._initialize(variable, value)

        Recorder.__init__(self, population=self)

    @property
    def first_id(self):
        return self.__first_id

    @property
    def last_id(self):
        return self.__last_id

    @property
    def _vertex(self):
        return self.__vertex

    @property
    def requires_mapping(self):
        return self.__change_requires_mapping

    @requires_mapping.setter
    def requires_mapping(self, new_value):
        self.__change_requires_mapping = new_value

    def mark_no_changes(self):
        self.__change_requires_mapping = False
        self.__has_read_neuron_parameters_this_run = False

    def __add__(self, other):
        """ Merges populations
        """
        # TODO: Make this add the neurons from another population to this one
        raise NotImplementedError


    @property
    def conductance_based(self):
        """ True if the population uses conductance inputs
        """
        if hasattr(self.__vertex, "conductance_based"):
            return self.__vertex.conductance_based
        return False

    # NON-PYNN API CALL
    def get_by_selector(self, selector, parameter_names):
        """ Get the values of a parameter for the selected cell in the\
            population.

        :param parameter_names: Name of parameter. This is either a\
            single string or a list of strings
        :param selector: a description of the subrange to accept. \
            Or None for all. \
            See: _selector_to_ids in \
            SpiNNUtils.spinn_utilities.ranged.abstract_sized.py
        :return: A single list of values (or possibly a single value) if\
            paramter_names is a string or a dict of these if parameter names\
            is a list.
        :rtype: str or list(str) or dict(str,str) or dict(str,list(str))
        """
        if not self._vertex_population_settable:
            raise KeyError("Population does not support setting")
        if isinstance(parameter_names, string_types):
            return self.__vertex.get_value_by_selector(
                selector, parameter_names)
        results = dict()
        for parameter_name in parameter_names:
            results[parameter_name] = self.__vertex.get_value_by_selector(
                selector, parameter_name)
        return results

    def id_to_index(self, id):  # @ReservedAssignment
        """ Given the ID(s) of cell(s) in the Population, return its (their)\
            index (order in the Population).
        """
        # pylint: disable=redefined-builtin
        if not numpy.iterable(id):
            if not self.__first_id <= id <= self.__last_id:
                raise ValueError(
                    "id should be in the range [{},{}], actually {}".format(
                        self.__first_id, self.__last_id, id))
            return int(id - self.__first_id)  # assume IDs are consecutive
        return id - self.__first_id

    def index_to_id(self, index):
        """ Given the index (order in the Population) of cell(s) in the\
            Population, return their ID(s)
        """
        if not numpy.iterable(index):
            if index > self.__last_id - self.__first_id:
                raise ValueError(
                    "indexes should be in the range [{},{}], actually {}"
                    "".format(0, self.__last_id - self.__first_id, index))
            return int(index + self.__first_id)
        # this assumes IDs are consecutive
        return index + self.__first_id

    def id_to_local_index(self, cell_id):
        """ Given the ID(s) of cell(s) in the Population, return its (their)\
            index (order in the Population), counting only cells on the local\
            MPI node.
        """
        # TODO: Need __getitem__
        raise NotImplementedError

    def _initialize(self, variable, value):
        """ Set the initial value of one of the state variables of the neurons\
            in this population.
        """
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation of {}".format(
                    variable))
        if globals_variables.get_not_running_simulator().has_ran \
                and not self._vertex_changeable_after_run:
            raise Exception("Population does not support changes after run")
        self._read_parameters_before_set()
        self.__vertex.initialize(variable, value)

    def can_record(self, variable):
        """ Determine whether `variable` can be recorded from this population.

        Note: This is supported by sPyNNaker8
        """

        # TODO: Needs a more precise recording mechanism (coming soon)
        raise NotImplementedError

    def inject(self, current_source):
        """ Connect a current source to all cells in the Population.
        """

        # TODO:
        raise NotImplementedError

    def __iter__(self):
        """ Iterate over local cells

        Note: This is supported by sPyNNaker8
        """

        # TODO:
        raise NotImplementedError

    def __len__(self):
        """ Get the total number of cells in the population.
        """
        return self._size

    @property
    def label(self):
        """ The label of the population
        """
        return self._vertex.label

    @label.setter
    def label(self, label):
        raise NotImplementedError(
            "As label is used as an ID it can not be changed")

    @property
    def local_size(self):
        """ The number of local cells
        """
        # Doesn't make much sense on SpiNNaker
        return self._size

    def _set_check(self, parameter, value):
        """ Checks for various set methods.
        """
        if not self._vertex_population_settable:
            raise KeyError("Population does not have property {}".format(
                parameter))

        if globals_variables.get_not_running_simulator().has_ran \
                and not self._vertex_changeable_after_run:
            raise Exception(
                " run has been called")

        if isinstance(parameter, string_types):
            if value is None:
                raise Exception("A value (not None) must be specified")
        elif type(parameter) is not dict:
            raise Exception(
                "Parameter must either be the name of a single parameter to"
                " set, or a dict of parameter: value items to set")

        self._read_parameters_before_set()

    def set(self, parameter, value=None):
        """ Set one or more parameters for every cell in the population.

        param can be a dict, in which case value should not be supplied, or a\
        string giving the parameter name, in which case value is the parameter\
        value. value can be a numeric value, or list of such\
        (e.g. for setting spike times)::

            p.set("tau_m", 20.0).
            p.set({'tau_m':20, 'v_rest':-65})

        :param parameter: the parameter to set
        :type parameter: str or dict
        :param value: the value of the parameter to set.
        """
        self._set_check(parameter, value)

        # set new parameters
        if isinstance(parameter, string_types):
            if value is None:
                raise Exception("A value (not None) must be specified")
            self.__vertex.set_value(parameter, value)
            return
        for (key, value) in parameter.iteritems():
            self.__vertex.set_value(key, value)

    # NON-PYNN API CALL
    def set_by_selector(self, selector, parameter, value=None):
        """ Set one or more parameters for selected cell in the population.

        param can be a dict, in which case value should not be supplied, or a\
        string giving the parameter name, in which case value is the parameter\
        value. value can be a numeric value, or list of such
        (e.g. for setting spike times)::

            p.set("tau_m", 20.0).
            p.set({'tau_m':20, 'v_rest':-65})

        :param selector: See RangedList.set_value_by_selector as this is just \
            a pass through method
        :param parameter: the parameter to set
        :param value: the value of the parameter to set.
        """
        self._set_check(parameter, value)

        # set new parameters
        if type(parameter) is str:
            self.__vertex.set_value_by_selector(selector, parameter, value)
        else:
            for (key, value) in parameter.iteritems():
                self.__vertex.set_value_by_selector(selector, key, value)

    def _read_parameters_before_set(self):
        """ Reads parameters from the machine before "set" completes

        :return: None
        """

        # If the tools have run before, and not reset, and the read
        # hasn't already been done, read back the data
        if globals_variables.get_simulator().has_ran \
                and self._vertex_read_parameters_before_set \
                and not self.__has_read_neuron_parameters_this_run \
                and not globals_variables.get_simulator().use_virtual_board:
            # locate machine vertices from the application vertices
            machine_vertices = globals_variables.get_simulator().graph_mapper\
                .get_machine_vertices(self.__vertex)

            # go through each machine vertex and read the neuron parameters
            # it contains
            for machine_vertex in machine_vertices:

                # tell the core to rewrite neuron params back to the
                # SDRAM space.
                placement = globals_variables.get_simulator().placements.\
                    get_placement_of_vertex(machine_vertex)

                self.__vertex.read_parameters_from_machine(
                    globals_variables.get_simulator().transceiver, placement,
                    globals_variables.get_simulator().graph_mapper.get_slice(
                        machine_vertex))

            self.__has_read_neuron_parameters_this_run = True


    @property
    def positions(self):
        """ Return the position array for structured populations.
        """
        if self._positions is None:
            if self.__structure is None:
                raise ValueError("attempted to retrieve positions "
                                 "for an unstructured population")
            self._positions = self.__structure.generate_positions(
                self.__vertex.n_atoms)
        return self._positions

    @property
    def structure(self):
        """ Return the structure for the population.
        """
        return self.__structure

    # NON-PYNN API CALL
    def set_constraint(self, constraint):
        """ Apply a constraint to a population that restricts the processor\
            onto which its atoms will be placed.
        """
        globals_variables.get_simulator().verify_not_running()
        if not isinstance(constraint, AbstractConstraint):
            raise ConfigurationException(
                "the constraint entered is not a recognised constraint")

        self.__vertex.add_constraint(constraint)
        # state that something has changed in the population,
        self.__change_requires_mapping = True

    # NON-PYNN API CALL
    def add_placement_constraint(self, x, y, p=None):
        """ Add a placement constraint

        :param x: The x-coordinate of the placement constraint
        :type x: int
        :param y: The y-coordinate of the placement constraint
        :type y: int
        :param p: The processor ID of the placement constraint (optional)
        :type p: int
        """
        globals_variables.get_simulator().verify_not_running()
        self.__vertex.add_constraint(ChipAndCoreConstraint(x, y, p))

        # state that something has changed in the population,
        self.__change_requires_mapping = True

    # NON-PYNN API CALL
    def set_max_atoms_per_core(self, max_atoms_per_core):
        """ Supports the setting of this population's max atoms per core

        :param max_atoms_per_core: the new value for the max atoms per core.
        """
        globals_variables.get_simulator().verify_not_running()
        self.__vertex.add_constraint(
            MaxVertexAtomsConstraint(max_atoms_per_core))
        # state that something has changed in the population
        self.__change_requires_mapping = True

    @property
    def size(self):
        """ The number of neurons in the population
        """
        return self.__vertex.n_atoms

    @property
    def _get_vertex(self):
        return self.__vertex

    @property
    def _internal_delay_vertex(self):
        return self.__delay_vertex

    @_internal_delay_vertex.setter
    def _internal_delay_vertex(self, delay_vertex):
        self.__delay_vertex = delay_vertex
        self.__change_requires_mapping = True

    def __iter__(self):
        """ Iterate over local cells
        """
        for _id in range(self._size):
            yield IDMixin(self, _id)

    def __getitem__(self, index_or_slice):
        if isinstance(index_or_slice, int):
            return IDMixin(self, index_or_slice)
        else:
            return PopulationView(
                self, index_or_slice, label="view over {}".format(self.label))

    def all(self):
        """ Iterator over cell IDs on all MPI nodes."""
        for _id in range(self._size):
            yield IDMixin(self, _id)

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
        return self._celltype

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
            logger_utils.warn_once(
                logger, "record indexes parameter is non-standard PyNN, "
                "so may not be portable to other simulators. "
                "It is now deprecated and replaced with views")
        self._record_with_indexes(
            variables, to_file, sampling_interval, indexes)

    def _record_with_indexes(
            self, variables, to_file, sampling_interval, indexes):
        """ Same as record but without non-standard PyNN warning

        This method is non-standard PyNN and is intended only to be called by\
        record in a Population, View or Assembly
        """
        if variables is None:  # reset the list of things to record
            if sampling_interval is not None:
                raise ConfigurationException(
                    "Clash between parameters in record."
                    "variables=None turns off recording,"
                    "while sampling_interval!=None implies turn on recording")
            if indexes is not None:
                logger_utils.warn_once(
                    logger,
                    "View.record with variable None is non-standard PyNN. "
                    "Only the neurons in the view have their record turned "
                    "off. Other neurons already set to record will remain "
                    "set to record")

            # note that if record(None) is called, its a reset
            Recorder._turn_off_all_recording(self, indexes)
            # handle one element vs many elements
        elif isinstance(variables, string_types):
            # handle special case of 'all'
            if variables == "all":
                logger_utils.warn_once(
                    logger, 'record("all") is non-standard PyNN, and '
                    'therefore may not be portable to other simulators.')

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

    def sample(self, n, rng=None):
        """ Randomly sample `n` cells from the Population, and return a\
            PopulationView object.
        """
        if not rng:
            rng = NumpyRNG()
        indices = rng.permutation(
            numpy.arange(len(self), dtype=numpy.int))[0:n]
        return PopulationView(
            self, indices,
            label="Random sample size {} from {}".format(n, self.label))

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
            logger_utils.warn_once(
                logger, "sPyNNaker only supports gather=True. We will run "
                "as if gather was set to True.")

        if isinstance(io, string_types):
            io = neo.get_io(io)

        data = self._extract_neo_block(variables, None, clear, annotations)
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
            "first_id": self.first_id,
            "last_id": self.last_id,
        }
        context.update(self._annotations)
        if self.size > 0:
            context.update({
                "local_first_id": self.first_id,
                "cell_parameters": {}})
        if self.__structure:
            context["structure"] = self.__structure.describe(template=None)
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
        :param gather: Whether to collect data from all MPI nodes or just the\
            current node.

            .. note::
                This is irrelevant on sPyNNaker, which always behaves as if
                this parameter is True.

        :type gather: bool
        :param clear: \
            Whether recorded data will be deleted from the `Assembly`.
        :type clear: bool
        :param annotations: annotations to put on the neo block
        :type annotations: dict
        :rtype: neo.Block
        """
        if not gather:
            logger_utils.warn_once(
                logger, "sPyNNaker only supports gather=True. We will run "
                "as if gather was set to True.")

        return self._extract_neo_block(variables, None, clear, annotations)

    def get_data_by_indexes(
            self, variables, indexes, clear=False, annotations=None):
        """ Return a Neo `Block` containing the data\
            (spikes, state variables) recorded from the Assembly.

        :param variables: either a single variable name or a list of variable\
            names. Variables must have been previously recorded, otherwise an
            Exception will be raised.
        :type variables: str or list
        :param indexes: List of neuron indexes to include in the data.
            Clearly only neurons recording will actually have any data
            If None will be taken as all recording as get_data
        :type indexes: list (int)
        :param clear: Whether recorded data will be deleted.
        :type clear: bool
        :param annotations: annotations to put on the neo block
        :type annotations: dict
        :rtype: neo.Block
        """
        return self._extract_neo_block(variables, indexes, clear, annotations)

    def spinnaker_get_data(self, variable):
        """ Public accessor for getting data as a numpy array, instead of\
            the neo based object

        :param variable: \
            either a single variable name or a list of variable names.\
            Variables must have been previously recorded, otherwise an\
            Exception will be raised.
        :return: numpy array of the data
        """
        logger_utils.warn_once(
            logger, "spinnaker_get_data is non-standard PyNN and therefore "
            "may not be portable to other simulators. Nor do we guarantee "
            "that this function will exist in future releases.")
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
        n_spikes = {}
        counts = numpy.bincount(spikes[:, 0].astype(dtype=numpy.int32),
                                minlength=self.__vertex.n_atoms)
        for i in range(self.__vertex.n_atoms):
            n_spikes[i] = counts[i]
        return n_spikes

    def find_units(self, variable):
        """ Get the units of a variable

        :param variable: The name of the variable
        :return: The units of the variable
        """
        if self._vertex_contains_units:
            return self.__vertex.get_units(parameter_name)
        raise ConfigurationException(
            "This population does not support describing its units")

    def set(self, **kwargs):
        for parameter, value in iteritems(kwargs):
            try:
                super(Population, self).set(parameter, value)
            except InvalidParameterType:
                super(Population, self)._initialize(parameter, value)

    def tset(self, **kwargs):
        logger.warn(
            "This function is deprecated; call pop.set(...) instead")
        for parameter, value in iteritems(kwargs):
            try:
                super(Population, self).set(parameter, value)
            except InvalidParameterType:
                super(Population, self)._initialize(parameter, value)

    def initialize(self, **kwargs):
        for parameter, value in iteritems(kwargs):
            super(Population, self)._initialize(parameter, value)

    @property
    def initial_values(self):
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation")
        return self._vertex.initial_values

    # NON-PYNN API CALL
    def get_initial_value(self, variable, selector=None):
        """ See AbstractPopulationInitializable.get_initial_value
        """
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation of {}".format(
                    variable))
        return self._vertex.get_initial_value(variable, selector)

    # NON-PYNN API CALL
    def set_initial_value(self, variable, value, selector=None):
        """ See AbstractPopulationInitializable.set_initial_value
        """
        if not self._vertex_population_initializable:
            raise KeyError(
                "Population does not support the initialisation of {}".format(
                    variable))
        if globals_variables.get_not_running_simulator().has_ran \
                and not self._vertex_changeable_after_run:
            raise Exception("Population does not support changes after run")
        self._vertex.set_initial_value(variable, value, selector)

    # NON-PYNN API CALL
    def get_initial_values(self, selector=None):
        """ See AbstractPopulationInitializable.get_initial_values
        """
        if not self._vertex_population_initializable:
            raise KeyError("Population does not support the initialisation")
        return self._vertex.get_initial_values(selector)

    def get(self, parameter_names, gather=False, simplify=True):
        if simplify is not True:
            logger_utils.warn_once(
                logger, "The simplify value is ignored if not set to true")
        if not self._vertex_population_settable:
            raise KeyError("Population does not support setting")
        if isinstance(parameter_names, string_types):
            return self.__vertex.get_value(parameter_names)
        results = dict()
        for parameter_name in parameter_names:
            results[parameter_name] = self.__vertex.get_value(parameter_name)
        return results

    @property
    def positions(self):
        """ Return the position array for structured populations.
        """
        if self._positions is None:
            if self.__structure is None:
                raise ValueError("attempted to retrieve positions "
                                 "for an unstructured population")
            self._positions = self.__structure.generate_positions(
                self._vertex.n_atoms)
        return self._positions.T  # change of order in pyNN 0.8

    @positions.setter
    def positions(self, positions):
        """ Sets all the positions in the population.
        """
        self._positions = positions

        # state that something has changed in the population,
        self._change_requires_mapping = True

    @property
    def all_cells(self):
        cells = []
        for _id in range(self._size):
            cells.append(IDMixin(self, _id))
        return cells

    @property
    def position_generator(self):
        def gen(i):
            return self.positions[:, i]
        return gen

    @staticmethod
    def create(cellclass, cellparams=None, n=1):
        """ Pass through method to the constructor defined by PyNN.\
        Create n cells all of the same type.\
        Returns a Population object.

        :param cellclass: see Population.__init__
        :param cellparams: see Population.__init__
        :param n: see Population.__init__(size...)
        :return: A New Population
        """
        return Population(size=n, cellclass=cellclass, cellparams=cellparams)
