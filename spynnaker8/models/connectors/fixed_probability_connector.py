from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_probability_connector import FixedProbabilityConnector as \
    CommonFixedProbabilityConnector
from pyNN.connectors import FixedProbabilityConnector as \
    PyNNFixedProbabilityConnector


class FixedProbabilityConnector(
    CommonFixedProbabilityConnector, PyNNFixedProbabilityConnector):
    """
    For each pair of pre-post cells, the connection probability is constant.

    :param `float` p_connect:
        a float between zero and one. Each potential connection
        is created with this probability.
    :param `bool` allow_self_connections:
        if the connector is used to connect a
        Population to itself, this flag determines whether a neuron is
        allowed to connect to itself, or only to other neurons in the
        Population.
    :param weights:
        may either be a float or a !RandomDistribution object. Units nA.
    :param delays:
        If `None`, all synaptic delays will be set
        to the global minimum delay.
    :param `pyNN.Space` space:
        a Space object, needed if you wish to specify distance-
        dependent weights or delays - not implemented
    """

    def __init__(
            self, p_connect, weights=0.0, delays=1,
            allow_self_connections=True, safe=True, space=None,
            verbose=False, rng=None, callback=None):
        CommonFixedProbabilityConnector.__init__(
            self, p_connect=p_connect, weights=weights, delays=delays,
            allow_self_connections=allow_self_connections, safe=safe,
            space=space, verbose=verbose)
        PyNNFixedProbabilityConnector.__init__(
            self, p_connect=p_connect, callback=callback,
            allow_self_connections=allow_self_connections, rng=rng, safe=safe)

    @property
    def p_connect(self):
        return self._p_connect

    @p_connect.setter
    def p_connect(self, new_value):
        self._p_connect = new_value
