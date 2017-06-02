from pyNN.random import RandomDistribution
from pyNN.connectors import OneToOneConnector as PyNNOneToOneConnector

from spynnaker.pyNN.models.neural_projections.connectors\
    .one_to_one_connector import OneToOneConnector as CommonOneToOneConnector
# Exceptions
from spynnaker8.utilities.exceptions import PyNN7Exception


class OneToOneConnector(CommonOneToOneConnector, PyNNOneToOneConnector):
    """
    Where the pre- and postsynaptic populations have the same size, connect
    cell i in the presynaptic pynn_population.py to cell i in the postsynaptic
    pynn_population.py for all i.
    """

    def __init__(self, safe=True, callback=None, weight=None, delay=None):
        """

        :param safe:
        :param callback:
        :param weight: Must be None. Only listed to catch Pynn7 syntax
        :type weight None
        :param delay: Must be None. Only listed to catch Pynn7 syntax
        :type delay: None
        """
        if weight is not None:
            raise PyNN7Exception("weight is now set in the synapse_type")
        if delay is not None:
            raise PyNN7Exception("weight is now set in the synapse_type")

        CommonOneToOneConnector.__init__(
            self, safe=safe, random_number_class=RandomDistribution)
        PyNNOneToOneConnector.__init__(self, safe=safe, callback=callback)
