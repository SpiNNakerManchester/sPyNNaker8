from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_pre_connector import FixedNumberPreConnector as \
    CommonFixedNumberPreConnector
from pyNN.connectors import FixedNumberPreConnector as \
    PyNNFixedNumberPreConnector

import logging

logger = logging.getLogger(__file__)


class FixedNumberPreConnector(
    CommonFixedNumberPreConnector, PyNNFixedNumberPreConnector):
    """ Connects a fixed number of pre-synaptic neurons selected at random,
        to all post-synaptic neurons
    """

    def __init__(
            self, n, weights=0.0, delays=1, allow_self_connections=True,
            space=None, safe=True, verbose=False, with_replacement=False,
            rng=None, callback=None):
        """
        :param n:
            number of random pre-synaptic neurons connected to output
        :param allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :param weights:
            may either be a float, a !RandomDistribution object, a list/
            1D array with at least as many items as connections to be
            created. Units nA.
        :param delays:
            If `None`, all synaptic delays will be set
            to the global minimum delay.
        :param `pyNN.Space` space:
            a Space object, needed if you wish to specify distance-
            dependent weights or delays - not implemented
        :param safe:
        :param verbose:
        :param with_replacement:
        :param rng:
        :param callback:
        """
        CommonFixedNumberPreConnector.__init__(
            self, n=n, weights=weights, delays=delays, safe=safe,
            allow_self_connections=allow_self_connections, space=space,
            verbose=verbose)
        PyNNFixedNumberPreConnector.__init__(
            self, n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, rng=rng, safe=safe,
            callback=callback)
