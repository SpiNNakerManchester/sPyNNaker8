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

    def __init__(
            self, d_expression, allow_self_connections=True,  safe=True,
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
        :param `int` n_connections:
            The number of efferent synaptic connections per neuron.
        :param safe: if True, check that weights and delays have valid values.
         If False, this check is skipped.
        """

        CommonDistanceDependentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections,
            safe=safe, verbose=verbose, n_connections=n_connections)
        PyNNDistanceDepednentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections, rng=rng, safe=safe,
            callback=callback)
