from pacman.model.decorators.overrides import overrides

from pyNN.standardmodels import StandardCellType as PyNNStandardCellType

from spynnaker.pyNN.models.neuron.input_types.input_type_conductance import \
    InputTypeConductance


class BuildCommon(object):
    """ this class overrides the calls from the pynn cell base that depend
    on the parameters object (as we wont use that)

    """

    def __init__(self, vertex):
        self._vertex = vertex

    @overrides(
        PyNNStandardCellType.conductance_based,
        additional_comments=
        "Overrides this explicit call from PyNN, so that we can use our neuron"
        " parameter formats.")
    @property
    def conductance_based(self):
        return isinstance(self._vertex, InputTypeConductance)

    @overrides(
        PyNNStandardCellType.receptor_types,
        additional_comments=
        "Overrides this explicit call from PyNN, so that we can use our neuron"
        " parameter formats.")
    @property
    def receptor_types(self):
        return self._vertex.synapse_type

    @overrides(
        PyNNStandardCellType._get_cell_initial_value,
        additional_comments=
        "Overrides this explicit call from PyNN, so that we can use our neuron"
        " parameter formats.")
    def _get_cell_initial_value(self, id, variable):
        values = self._vertex.get_value(variable)
        return values[id]

    @overrides(
        PyNNStandardCellType._set_cell_initial_value,
        additional_comments=
        "Overrides this explicit call from PyNN, so that we can use our neuron"
        " parameter formats.")
    def _set_cell_initial_value(self, id, variable, value):
        self._vertex.set_value_at_index(variable, value, id)
