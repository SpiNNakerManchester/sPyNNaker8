from pyNN.space import Space

from pyNN.connectors import AllToAllConnector as PyNNAllToAllConnector

from spynnaker.pyNN.models.neural_projections.connectors. \
    all_to_all_connector import AllToAllConnector as CommonAllToAllConnector

import logging

logger = logging.getLogger(__file__)


class AllToAllConnector(CommonAllToAllConnector, PyNNAllToAllConnector):
    """ Connects all cells in the presynaptic population to all cells in \
        the postsynaptic population
    """

    def __init__(
            self, allow_self_connections=True, safe=True,
            verbose=None, callbacks=None):
        """

        :param allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :type allow_self_connections: bool
        :param safe: if True, check that weights and delays have valid values.
         If False, this check is skipped.
        :param verbose:
        :param callbacks:
    """
        CommonAllToAllConnector.__init__(
            self, allow_self_connections=allow_self_connections,
            safe=safe, verbose=verbose)
        PyNNAllToAllConnector.__init__(
            self, allow_self_connections=allow_self_connections, safe=safe,
            callback=callbacks)
