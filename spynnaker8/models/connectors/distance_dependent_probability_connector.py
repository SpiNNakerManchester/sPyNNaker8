from spynnaker.pyNN.models.neural_projections.connectors. \
    distance_dependent_probability_connector import \
    DistanceDependentProbabilityConnector as \
        CommonDistanceDependentProbabilityConnector

from pyNN.connectors import DistanceDependentProbabilityConnector as \
    PyNNDistanceDepednentProbabilityConnector
from pyNN.space import Space

from pacman.model.decorators.overrides import overrides


class DistanceDependentProbabilityConnector(
    CommonDistanceDependentProbabilityConnector,
    PyNNDistanceDepednentProbabilityConnector):
    """ Make connections using a distribution which varies with distance.
    """

    def __init__(self, d_expression, allow_self_connections=True,
                 weights=0.0, delays=1, space=Space(), safe=True,
                 verbose=False, n_connections=None, rng=None, callback=None):
        """

        :param `string` d_expression:
            the right-hand side of a valid python expression for
            probability, involving 'd', e.g. "exp(-abs(d))", or "d<3",
            that can be parsed by eval(), that computes the distance
            dependent distribution
        :param `bool` allow_self_connections:
            if the connector is used to connect a
            Population to itself, this flag determines whether a neuron is
            allowed to connect to itself, or only to other neurons in the
            Population.
        :param `float` weights:
            may either be a float, a !RandomDistribution object, a list/
            1D array with at least as many items as connections to be
            created, or a distance dependence as per a d_expression. Units nA.
        :param `float` delays:  -- as `weights`. If `None`, all synaptic delays
            will be set to the global minimum delay.
        :param `pyNN.Space` space:
            a Space object, needed if you wish to specify distance-
            dependent weights or delays
        :param `int` n_connections:
            The number of efferent synaptic connections per neuron.
        """

        CommonDistanceDependentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections, weights=weights,
            delays=delays, space=space, safe=safe, verbose=verbose,
            n_connections=n_connections)
        PyNNDistanceDepednentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections, rng=rng, safe=safe,
            callback=callback)
