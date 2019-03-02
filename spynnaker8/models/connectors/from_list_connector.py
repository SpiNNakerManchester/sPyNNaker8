from pyNN.connectors import Connector
from spynnaker.pyNN.models.neural_projections.connectors import (
    FromListConnector as CommonFromListConnector)


class FromListConnector(CommonFromListConnector, Connector):
    """ Make connections according to a list.
    """
    __slots__ = []

    def __init__(
            self, conn_list, safe=True, verbose=False, column_names=None,
            callback=None):
        """
        :param conn_list: \
            a list of tuples, one tuple for each connection. Each tuple\
            should contain: `(pre_idx, post_idx, p1, p2, ..., pn)` where\
            `pre_idx` is the index (i.e. order in the Population, not the ID)\
            of the presynaptic neuron, `post_idx` is the index of the\
            postsynaptic neuron, and `p1`, `p2`, etc. are the synaptic\
            parameters (e.g., weight, delay, plasticity parameters).
        :param column_names: \
            the names of the parameters p1, p2, etc. If not provided, it is\
            assumed the parameters are weight, delay (for\
            backwards compatibility).
        :param safe: \
            if True, check that weights and delays have valid values. If\
            False, this check is skipped.
        :param callback: \
            if given, a callable that display a progress bar on the terminal.
        """
        CommonFromListConnector.__init__(
            self, conn_list=conn_list, safe=safe, verbose=verbose,
            column_names=column_names)
        Connector.__init__(self, safe=safe, callback=callback)
