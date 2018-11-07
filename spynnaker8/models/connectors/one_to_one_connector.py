from pyNN.random import RandomDistribution
from pyNN.connectors import OneToOneConnector as PyNNOneToOneConnector

from spynnaker.pyNN.models.neural_projections.connectors \
    import OneToOneConnector as CommonOneToOneConnector


class OneToOneConnector(CommonOneToOneConnector, PyNNOneToOneConnector):
    """
    Where the pre- and postsynaptic populations have the same size, connect\
    cell i in the presynaptic population to cell i in the postsynaptic\
    population for all i.
    """
    __slots__ = []

    def __init__(self, safe=True, callback=None):
        """
        :param safe: if True, check that weights and delays have valid values.\
            If False, this check is skipped.
        :param callback: a function that will be called with the fractional \
            progress of the connection routine. An example would be \
            progress_bar.set_level.
        """
        CommonOneToOneConnector.__init__(
            self, safe=safe, random_number_class=RandomDistribution)
        PyNNOneToOneConnector.__init__(self, safe=safe, callback=callback)
