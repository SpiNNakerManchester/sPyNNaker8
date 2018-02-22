# Alternative implemenation for
# https://github.com/NeuralEnsemble/PyNN/blob/master/pyNN/common/populations.py

class IDMixin(object):
    __slots__ = ["_id", "_population"]

    def __init__(self, population, id):
        self._id = id
        self._population = population

    def __getattr__(self, name):
        #if name in self.__slots__:
        #    object.__getattr__(self, name)
        return self._population.get_by_selector(self._id, name)

    def __setattr__(self, name, value):
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            self._population.set_by_selector(self._id, name, value)

    def set_parameters(self, **parameters):
        """
        Set cell parameters, given as a sequence of parameter=value arguments.
        """
        for (name, value) in parameters.iteritems():
            self._population.set_by_selector(self._id, name, value)

    def get_parameters(self):
        """Return a dict of all cell parameters."""
        results = dict()
        for name in self.celltype.get_parameter_names():
            results[name] = self._population.get_by_selector(self._id, name)
        return results

    @property
    def celltype(self):
        return self._population.celltype

    @property
    def is_standard_cell(self):
        raise NotImplementedError  # pragma: no cover

    def _set_position(self, pos):
        """
        Set the cell position in 3D space.
        Cell positions are stored in an array in the parent Population.
        """
        self._population.positions[self._id] = pos   # pragma: no cover

    def _get_position(self):
        """
        Return the cell position in 3D space.
        Cell positions are stored in an array in the parent Population, if any,
        or within the ID object otherwise. Positions are generated the first
        time they are requested and then cached.
        """
        return self._population.positions[:, self._id]   # pragma: no cover

    position = property(_get_position, _set_position)

    @property
    def local(self):
        return self._population.is_local(self._id)

    def inject(self, current_source):
        """Inject current from a current source object into the cell."""
        raise NotImplementedError  # pragma: no cover

    def get_initial_value(self, variable):
        """Get the initial value of a state variable of the cell."""
        return self._population.get_initial_value(variable, self._id)

    def set_initial_value(self, variable, value):
        """Set the initial value of a state variable of the cell."""
        self._population.set_initial_value(variable, value, self._id)

    def as_view(self):
        """Return a PopulationView containing just this cell."""
        return self._population[self._id]
