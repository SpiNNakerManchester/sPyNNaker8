import logging

from spynnaker.pyNN.models.neural_projections.connectors \
    import FixedNumberPostConnector as CommonFixedNumberPostConnector
from pyNN.connectors import FixedNumberPostConnector as \
    PyNNFixedNumberPostConnector

logger = logging.getLogger(__file__)


class FixedNumberPostConnector(CommonFixedNumberPostConnector,
                               PyNNFixedNumberPostConnector):
    """ pynn connector that puts a fixed number of connections on each of the
     post neurons

    """

    def __init__(
            self, n, allow_self_connections=True, safe=True, verbose=False,
            with_replacement=False, rng=None, callback=None):
        """

        :param n:
            number of random post-synaptic neurons connected to output
        :param allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :param safe: if True, check that weights and delays have valid values;
            if False, this check is skipped.
        :param verbose: if True, outputs extra information about the
            connectivity to a csv file
        :param with_replacement:
            if False, once a connection is made, it can't be
            made again; if True, multiple connections between the same pair
            of neurons are allowed
        :param rng: random number generator
        :param callback: list of callbacks to run
        """
        CommonFixedNumberPostConnector.__init__(
            self, n=n, allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, safe=safe, verbose=verbose)
#        PyNNFixedNumberPostConnector.__init__(
#            self, n=n, allow_self_connections=allow_self_connections,
#            with_replacement=with_replacement, rng=rng, safe=safe,
#            callback=callback)

    def get_rng_parameters(self, n_post_neurons):
        return {"low": 0, "high": n_post_neurons}
