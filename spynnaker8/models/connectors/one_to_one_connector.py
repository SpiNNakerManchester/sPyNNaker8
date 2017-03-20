from pyNN.space import Space
from pyNN.random import RandomDistribution
from pyNN.connectors import OneToOneConnector as PyNNOneToOneConnector

from spynnaker.pyNN.models.neural_projections.connectors\
    .one_to_one_connector import OneToOneConnector as CommonOneToOneConnector


class OneToOneConnector(CommonOneToOneConnector, PyNNOneToOneConnector):
    """
    Where the pre- and postsynaptic populations have the same size, connect
    cell i in the presynaptic pynn_population.py to cell i in the postsynaptic
    pynn_population.py for all i.
    """

    def __init__(
            self, safe=True, callback=None):
        """
        """
        CommonOneToOneConnector.__init__(
            self, safe=safe, random_number_class=RandomDistribution)
        PyNNOneToOneConnector.__init__(self, safe=safe, callback=callback)

