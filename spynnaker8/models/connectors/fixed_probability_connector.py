from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_probability_connector import FixedProbabilityConnector as \
    CommonFixedProbabilityConnector
from pyNN.connectors import FixedProbabilityConnector as \
    PyNNFixedProbabilityConnector


class FixedProbabilityConnector(
        CommonFixedProbabilityConnector, PyNNFixedProbabilityConnector):
    """
    """

    def __init__(
            self, p_connect, allow_self_connections=True, safe=True,
            verbose=False, rng=None, callback=None):
        """ For each pair of pre-post cells, the connection probability is
         constant.

        :param p_connect: a float between zero and one. Each potential
        connection is created with this probability.
        :param allow_self_connections: if the connector is used to connect a
        Population to itself, this flag determines whether a neuron is
        allowed to connect to itself, or only to other neurons in the
        Population.
        :param safe: if True, check that weights and delays have valid values.
         If False, this check is skipped.
        :param space: a Space object, needed if you wish to specify distance-
        dependent weights or delays - not implemented
        :param verbose:
        :param rng:
        :param callback:
        """
        CommonFixedProbabilityConnector.__init__(
            self, p_connect=p_connect,
            allow_self_connections=allow_self_connections, safe=safe,
            verbose=verbose)
        PyNNFixedProbabilityConnector.__init__(
            self, p_connect=p_connect, callback=callback,
            allow_self_connections=allow_self_connections, rng=rng, safe=safe)

    def set_weights_and_delays(self, weights, delays):
        self._weights = weights
        self._delays = delays
        self._check_parameters(weights, delays, allow_lists=False)

    @property
    def p_connect(self):
        return self._p_connect

    @p_connect.setter
    def p_connect(self, new_value):
        self._p_connect = new_value
