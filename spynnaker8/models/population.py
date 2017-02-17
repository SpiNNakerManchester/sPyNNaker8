from pyNN import common as pynn_common
from pyNN.common.populations import PopulationView as PyNNPopulationView
from pyNN.parameters import ParameterSpace as PyNNParameterSpace
from pyNN.common.populations import Assembly as PyNNAssembly

from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.utilities import utility_calls

from spynnaker8.models.recorder import Recorder
from spynnaker8.utilities import globals_variables


class Population(pynn_common.Population, PyNNPopulationCommon):
    """ pynn 0.8 population object

    """

    __doc__ = pynn_common.Population.__doc__
    _simulator = None
    _recorder_class = None
    _assembly_class = None

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 initial_values=None, label=None):

        # hard code initial values as required
        if initial_values is None:
            initial_values = {}

        # fix pynn centric stuff
        self._simulator = globals_variables.get_simulator()
        self._recorder_class = self._recorder_class_builder
        self._recorder = None
        self._assembly_class = self._assembly_class_builder

        # build our initial objects
        PyNNPopulationCommon.__init__(
            self, spinnaker_control=self._simulator, size=size,
            cellclass=cellclass, cellparams=cellparams, label=label)

        # build pynn centric object
        pynn_common.Population.__init__(
            self, size, cellclass, cellparams, structure, initial_values,
            label)

    def _create_cells(self):
        """ enforced upon us due to pynn. Would be helpful when using
         pop views and assemblers

        :return: None
        """

        pass

    def _set_initial_value_array(self, variable, initial_values):
        """ forced method from pynn. is used during pynns initialize
        functionality. so we should migrate this to the vertex till pop views
        and assemblers are added

        :param variable: the name of the variable to change
        :param initial_values: the values to change to
        :return: None
        """
        self._vertex.initialize(
            variable, utility_calls.convert_param_to_numpy(
                initial_values, self._vertex.n_atoms))

    def _get_view(self, selector, label=None):
        """ enforced from pynn. is used during get item and sample.
        generates a PopulationView object.

        :param selector: the selection of atoms from the population to
        convert into a population view
        :param label: label of the new pop view.
        :return: a PopulationView object
        """
        return PyNNPopulationView(self, selector, label)

    def _get_parameters(self, *names):
        """ enforced from pynn. is used during get and set(why set???!)
        return a ParameterSpace containing native parameters
        """
        parameter_dict = {}
        for parameter_name in names:
            parameter_dict[parameter_name] = \
                self._vertex.get_value(parameter_name)
        return PyNNParameterSpace(parameter_dict, shape=(self.local_size,))

    def _set_parameters(self, parameter_space):
        """ enforced by PyNN. is used during its set.

        :param parameter_space: the names and values for parameters to set.
        :return: None
        """

        # Loop through values we're setting and
        # deep copy into our parameter space
        for parameter_name, value in parameter_space.items():
            self._vertex.set_vaue(parameter_name, value)

    @property
    def label(self):
        return self._vertex.label

    @label.setter
    def label(self, new_value):
        self._vertex.label = new_value

    def _assembly_class_builder(self, other):
        """ enforced by pynn. this builds an assembly from a pop and something
        using a indirect call to support extra params if needed

        :param other: a pop, pop view, or assembly.
        :return: An assembly
        """
        return PyNNAssembly([self, other])

    def _recorder_class_builder(self, population, output_file):
        """ enforced by pynn. this builds a recorder for a population and uses
        a indirect call to support extra params if needed

        :param population: the population this recorder is for
        :param output_file: the file to write data to or None if no file to
         write to
        :return: the recorder class
        """
        if self._recorder is None:
            self._recorder = Recorder(population, output_file)
        return self._recorder
