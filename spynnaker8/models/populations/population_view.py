import logging
from pyNN import descriptions

from spinn_utilities.ranged.abstract_sized import AbstractSized
from spynnaker8.models.populations import IDMixin, PopulationBase
logger = logging.getLogger(__name__)


class PopulationView(PopulationBase):

    def __init__(self, parent, selector, label=None):
        """
        A view of a subset of neurons within a Population.

        In most ways, Populations and PopulationViews have the same behaviour,
            i.e.they can be recorded, connected with Projections, etc.
        It should be noted that any changes to neurons in a PopulationView
            will be reflected in the parent Population and vice versa.

        It is possible to have views of views.

        param selector: a slice or numpy mask array.
            The mask array should either be a boolean array (ideally) of the
            same size as the parent,
            or an integer array containing cell indices,
            i.e. if  p.size == 5:
                PopulationView(p, array([False, False, True, False, True]))
                PopulationView(p, array([2, 4]))
                PopulationView(p, slice(2, 5, 2))
           will all create the same view.

        Note: Selector to Id is actually handled by AbstractSized.
        """
        self._parent = parent
        sized = AbstractSized(parent.size)
        ids = sized.selector_to_ids(selector, warn=True)

        if isinstance(parent, PopulationView):
            self._population =  parent.grandparent
            self._indexes = parent.index_in_grandparent(ids)
        else:
            self._population = parent
            self._indexes = ids
        self._mask = selector
        self._label = label
        self._annotations = dict()

    @property
    def size(self):
        """The total number of neurons in the Population."""
        return len(self._indexes)

    @property
    def label(self):
        """A label for the Population."""
        return self._label

    @property
    def celltype(self):
        """ The type of neurons making up the Population."""
        return self._population.celltype

    @property
    def initial_values(self):
        """ A dict containing the initial values of the state variables"""
        return self._population.get_initial_values(selector=self._indexes)

    @property
    def parent(self):
        """ A reference to the parent Population(that this is a view of)."""
        return self._parent

    @property
    def mask(self):
        """  The selector mask that was used to create this view."""
        return self._mask

    @property
    def all_cells(self):
        """  An array containing the cell ids of all neurons in the
            Population(all MPI nodes). """
        cells = []
        for id in self._indexes:
            cells.append(IDMixin(self._population, id))
        return cells

    def __getitem__(self, index):
        """
        Return either a single cell(ID object) from the Population,
            if index is an integer, or a subset of the cells
            (PopulationView object), if index is a slice or array.

        Note that __getitem__ is called when using[] access, e.g. p =
            Population(...) p[2] is equivalent to p.__getitem__(2).p[3:6] is
            equivalent to p.__getitem__(slice(3, 6))
        """
        if isinstance(index, (int, long)):
            return IDMixin(self._population, index)
        else:
            return PopulationView(self, index, label=self.label+"_" + str(
                index))

    def __iter__(self):
        """ Iterator over cell ids on the local node."""
        for id in self._indexes:
            yield IDMixin(self, id)

    def __len__(self):
        """  Return the total number of cells in the population(all nodes)."""
        return len(self._indexes)

    def all(self):
        """ Iterator over cell ids on all MPI nodes."""
        for id in self._indexes:
            yield IDMixin(self, id)

    def can_record(self, variable):
        """ Determine whether variable can be recorded from this population."""
        return self._population.can_record(variable)

    @property
    def conductance_based(self):
        """
        Indicates whether the post - synaptic response is modelled as a
        change in conductance or a change in current.
        """
        return self._population.conductance_based

    def describe(self, template='populationview_default.txt',
                 engine='default'):
        """ Returns a human - readable description of the population view.

        The output may be customized by specifying a different template
            togther with an associated template engine (see pyNN.descriptions).

        If template is None, then a dictionary containing the template
            context will be returned.
        """
        context = {"label": self.label,
                   "parent": self.parent.label,
                   "mask": self.mask,
                   "size": self.size}
        context.update(self._annotations)
        return descriptions.render(engine, template, context)

    def find_units(self, variable):
        """ NO PyNN description of this method """
        return self._population.find_units(variable)

    def get(self, parameter_names, gather=False, simplify=True):
        """
        Get the values of the given parameters for every local cell in
            the population, or, if gather=True,
            for all cells in the population.

        Values will be expressed in the standard PyNN units(i.e.millivolts,
        nanoamps, milliseconds, microsiemens, nanofarads, event per second).
        """
        if simplify is not True:
            logger.warning("The simplify value is ignored if not set to true")

        return self._population.get_by_selector(self._indexes, parameter_names)

    def get_data(self, variables='all', gather=True, clear=False):
        """
        Return a Neo Block containing the data(spikes, state variables)
            recorded from the Population.

        variables - either a single variable name or a list of variable names

        Variables must have been previously recorded,
            otherwise an Exception will be raised.

        For parallel simulators, if gather is True, all data will be
            gathered to all nodes and the Neo Block will contain data
            from all nodes.
        Otherwise, the Neo Block will contain only data from the cells
            simulated on the local node.

        If clear is True, recorded data will be deleted from the Population.
        """
        # TODO

    def get_spike_counts(self, gather=True):
        """ Returns a dict containing the number of spikes for each neuron.

        The dict keys are neuron IDs, not indices.
        """
        # TODO

    @property
    def grandparent(self):
        """
        Returns the parent Population at the root of the tree(since the
            immediate parent may itself be a PopulationView).

        The name "grandparent" is of course a little misleading, as it could
            be just the parent, or the great, great, great, ..., grandparent.
        """
        return self._population

    def id_to_index(self, id):
        """
        Given the ID(s) of cell(s) in the PopulationView, return its /
            their index / indices(order in the PopulationView).

        assert pv.id_to_index(pv[3]) == 3
        """
        if isinstance(id, (int, long)):
            return self._indexes.index(id)
        else:
            result = []
            for _id in id:
                result.append(self._indexes.index(_id))
            return result

    def index_in_grandparent(self, indices):
        """
        Given an array of indices, return the indices in the parent
            population at the root of the tree.
        """
        result = []
        for index in indices:
            result.append(self._indexes[index])
        return result

    def initialize(self, **initial_values):
        """
        Set initial values of state variables, e.g.the membrane potential.

        Values passed to initialize() may be:
            single numeric values(all neurons set to the same value)
        RandomDistribution objects
        lists / arrays of numbers of the same size as the population
        mapping functions, where a mapping function accepts a single
            argument(the cell index) and returns a single number.

        Values should be expressed in the standard PyNN units(
           i.e.millivolts, nanoamps, milliseconds, microsiemens, nanofarads,
           event per second).

        Examples:
            p.initialize(v=-70.0)
            p.initialize(v=rand_distr, gsyn_exc=0.0)
            p.initialize(v=lambda i: -65 + i / 10.0)
        """
        for variable, value in initial_values.iteritems():
            self._population.set_initial_value(variable, value, self._indexes)

    def record(self, variables, to_file=None, sampling_interval=None):
        """
        Record the specified variable or variables for all cells in the
            Population or view.

        variables may be either a single variable name or a list of variable
            names.
        For a given celltype class , celltype.recordable contains a list of
            variables that can be recorded for that celltype.

        If specified, to_file should be a Neo IO instance and write_data()
            will be automatically called when end() is called.

        sampling_interval should be a value in milliseconds, and an integer
            multiple of the simulation timestep.
        """
        # TODO

    def sample(self, n, rng=None):
        """
        Randomly sample n cells from the Population, and return a
            PopulationView object.
        """
        if not rng:
            rng = random.NumpyRNG()
        indices = rng.permutation(numpy.arange(len(self), dtype=numpy.int))[0:n]

    def set(self, **parameters):
        """
        Set one or more parameters for every cell in the population.

        Values passed to set() may be:
            single values
            RandomDistribution objects
            lists / arrays of values of the same size as the population
            mapping functions, where a mapping function accepts a single
                argument(the cell index) and returns a single value.

        Here, a "single value" may be either a single number or a list /
            array of numbers(e.g. for spike times).

        Values should be expressed in the standard PyNN units
            (i.e.millivolts, nanoamps, milliseconds, microsiemens, nanofarads,
            event per second).

        Examples:
            p.set(tau_m=20.0, v_rest=-65).
            p.set(spike_times=[0.3, 0.7, 0.9, 1.4])
            p.set(cm=rand_distr, tau_m=lambda i: 10 + i / 10.0)
        """
        for (parameter, value) in parameters.iteritems():
            self._population.set_by_selector(
                selector=self._indexes, parameter=parameter, value=value)

    def write_data(self, io, variables='all', gather=True, clear=False,
                   annotations=None):
        """
        Write recorded data to file, using one of the file formats
            supported by Neo.

        io: a Neo IO instance variables: either a single variable name or a
            list of variable names.

        Variables must have been previously recorded, otherwise an Exception
            will be raised.

        For parallel simulators, if gather is True, all data will be
            gathered to the master node and a single output file created there.
            Otherwise, a file will be written on each node,
            containing only data from the cells simulated on that node.

        If clear is True, recorded data will be deleted from the Population.

        annotations should be a dict containing simple data types such as
            numbers and strings. The contents will be written into the output
            data file as metadata.
        """
