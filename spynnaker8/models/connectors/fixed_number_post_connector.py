import logging

from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_post_connector import FixedNumberPostConnector as \
    CommonFixedNumberPostConnector
from pyNN.connectors import FixedNumberPostConnector as \
    PyNNFixedNumberPostConnector

logger = logging.getLogger(__file__)


class FixedNumberPostConnector(
    CommonFixedNumberPostConnector, PyNNFixedNumberPostConnector):
    def __init__(
            self, n, weights=0.0, delays=1, allow_self_connections=True,
            space=None, safe=True, verbose=False, with_replacement=False,
            rng=None, callback=None):
        """

        :param n: number of random post-synaptic neurons connected to output
        :param weights:
            may either be a float, a !RandomDistribution object, a list/
            1D array with at least as many items as connections to be
            created. Units nA.
        :param delays:
            If `None`, all synaptic delays will be set
            to the global minimum delay.
        :param allow_self_connections: ??????
        :param space: the space object for pynn
        :param safe: ??????????
        :param verbose: ??????????
        :param with_replacement:
            boolean that flags if once a connection is made, if it cant be
            made again
        :param rng: random number generator
        :param callback: list of callbacks to run
        """
        CommonFixedNumberPostConnector.__init__(
            self, n=n, weights=weights, delays=delays, safe=safe,
            allow_self_connections=allow_self_connections, space=space,
            verbose=verbose)
        PyNNFixedNumberPostConnector.__init__(
            self, n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, rng=rng, safe=safe,
            callback=callback)
