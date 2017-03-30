from spynnaker.pyNN.models.neuron.synapse_dynamics.\
    synapse_dynamics_stdp import SynapseDynamicsSTDP as \
    CommonSynapseDynamicsSTDP
from spynnaker.pyNN.utilities import globals_variables

TIME_STAMP_BYTES = 4

# When not using the MAD scheme, how many pre-synaptic events are buffered
NUM_PRE_SYNAPTIC_EVENTS = 4


class SynapseDynamicsSTDP(CommonSynapseDynamicsSTDP):

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

        self._weight = weight
        self._delay = delay

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
