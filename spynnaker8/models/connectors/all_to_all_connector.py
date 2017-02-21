from pacman.model.decorators.overrides import overrides

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
            self, weights=0.0, delays=1, allow_self_connections=True,
            space=None, safe=True, verbose=None, callbacks=None):
        """

        :param allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :type allow_self_connections: bool
        :param  weights:
            may either be a float, a !RandomDistribution object, a list/
            1D array with at least as many items as connections to be
            created. Units nA.
            :type weights: float
        :param delays:  -- as `weights`. If `None`, all synaptic delays
            will be set to the global minimum delay.
        :type delays: float
        :param space:
        :param safe:
        :param verbose:
        :param callbacks:
    """
        CommonAllToAllConnector.__init__(
            self, weights, delays, allow_self_connections, space, safe,
            verbose)
        PyNNAllToAllConnector.__init__(
            self, allow_self_connections=allow_self_connections, safe=safe,
            callback=callbacks)
