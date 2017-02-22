import logging

from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_post_connector import FixedNumberPostConnector as \
    CommonFixedNumberPostConnector
from pyNN.connectors import FixedNumberPostConnector as \
    PyNNFixedNumberPostConnector

logger = logging.getLogger(__file__)


class FixedNumberPostConnector(
    CommonFixedNumberPostConnector, PyNNFixedNumberPostConnector):
    """ pynn connector that puts a fixed number of connections on each of the
     post neurons

    """

    def __init__(
            self, n, allow_self_connections=True,
            space=None, safe=True, verbose=False, with_replacement=False,
            rng=None, callback=None):
        """

        :param n: number of random post-synaptic neurons connected to output
        :type n: int
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
            self, n=n, safe=safe, verbose=verbose,
            allow_self_connections=allow_self_connections, space=space)
        PyNNFixedNumberPostConnector.__init__(
            self, n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, rng=rng, safe=safe,
            callback=callback)
