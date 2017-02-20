import numpy

from pyNN import common as pynn_common
from pyNN.parameters import simplify, ParameterSpace
from spynnaker.pyNN.utilities import globals_variables
from spynnaker8.models.populations.assembly import Assembly


class PopulationView(pynn_common.PopulationView):
    _assembly_class = Assembly
    _simulator = globals_variables.get_simulator()

    # --------------------------------------------------------------------------
    # Internal PyNN methods
    # --------------------------------------------------------------------------
    def _get_parameters(self, *names):
        """
        return a ParameterSpace containing native parameters
        """
        parameter_dict = {}
        for name in names:
            value = self.parent._parameters[name]
            if isinstance(value, numpy.ndarray):
                value = value[self.mask]
            parameter_dict[name] = simplify(value)
        return ParameterSpace(parameter_dict, shape=(self.size,))

    def _set_parameters(self, parameter_space):
        # Loop through parameters we're setting, evaluate the value we're
        # Setting and assign it to the masked section of
        # parent's parameters this view represents
        for name, value in parameter_space.items():
            evaluated_value = value.evaluate(simplify=True)
            self.parent._parameters[name][self.mask] = evaluated_value

    def _set_initial_value_array(self, variable, initial_values):
        # Initial values are handled by common.Population
        # so we can evaluate them at build-time
        pass

    def _get_view(self, selector, label=None):
        return PopulationView(self, selector, label)
