from spinn_front_end_common.abstract_models.\
    abstract_changable_after_run import AbstractChangableAfterRun
from spinn_utilities.overrides import overrides
from spynnaker.pyNN import exceptions

# How large are the time-stamps stored with each event
from spynnaker.pyNN.models.abstract_models.\
    abstract_population_settable import \
    AbstractPopulationSettable
from spynnaker.pyNN.models.neuron.synapse_dynamics.\
    synapse_dynamics_stdp import SynapseDynamicsSTDP as \
    CommonSynapseDynamicsSTDP
from spynnaker.pyNN.utilities import globals_variables

TIME_STAMP_BYTES = 4

# When not using the MAD scheme, how many pre-synaptic events are buffered
NUM_PRE_SYNAPTIC_EVENTS = 4


class SynapseDynamicsSTDP(
        CommonSynapseDynamicsSTDP, AbstractPopulationSettable):

    def __init__(
            self, timing_dependence=None, weight_dependence=None,
            voltage_dependence=None, dendritic_delay_fraction=1.0,
            weight=0.0, delay=None):

        # move data from timing to weight dependence over as needed to reflect
        # standard structure underneath

        a_plus = timing_dependence.A_plus
        a_minus = timing_dependence.A_minus
        weight_dependence.set_a_plus_a_minus(a_plus=a_plus, a_minus=a_minus)

        if delay is None:
            delay = globals_variables.get_simulator().min_delay

        # instantiate common functionality.
        CommonSynapseDynamicsSTDP.__init__(
            self, timing_dependence=timing_dependence,
            weight_dependence=weight_dependence,
            voltage_dependence=voltage_dependence,
            dendritic_delay_fraction=dendritic_delay_fraction)
        AbstractPopulationSettable.__init__(self)

        self._weight = weight
        self._delay = delay
        self._change_requires_mapping = True

    @overrides(AbstractPopulationSettable.get_value)
    def get_value(self, key):
        """ Get a property
        """
        for obj in [self._timing_dependence, self._weight_dependence, self]:
            if hasattr(obj, key):
                return getattr(obj, key)
        raise exceptions.InvalidParameterType(
            "Type {} does not have parameter {}".format(self._model_name, key))

    @overrides(AbstractPopulationSettable.set_value)
    def set_value(self, key, value):
        """ Set a property

        :param key: the name of the parameter to change
        :param value: the new value of the parameter to assign
        """
        for obj in [self._timing_dependence, self._weight_dependence, self]:
            if hasattr(obj, key):
                setattr(obj, key, value)
                self._change_requires_mapping = True
        raise exceptions.InvalidParameterType(
            "Type {} does not have parameter {}".format(self._model_name, key))

    @overrides(AbstractChangableAfterRun.requires_mapping)
    def requires_mapping(self):
        """ True if changes that have been made require that mapping be\
            performed.  Note that this should return True the first time it\
            is called, as the vertex must require mapping as it has been\
            created!
        """
        return self._change_requires_mapping

    @overrides(AbstractChangableAfterRun.mark_no_changes)
    def mark_no_changes(self):
        """ Marks the point after which changes are reported.  Immediately\
            after calling this method, requires_mapping should return False.
        """
        self._change_requires_mapping = False

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_value):
        self._weight = new_value

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, new_value):
        self._delay = new_value
