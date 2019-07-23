from spynnaker.pyNN.models.neural_projections.connectors import (
    IndexBasedProbabilityConnector as CommonIndexBasedProbabilityConnector)


class IndexBasedProbabilityConnector(CommonIndexBasedProbabilityConnector):
    """
    Create an index-based probability connector.
    The index_expression must depend on the indices i, j of the populations.

    :param index_expression: a function of the indices of the populations
        An expression
    :type index_expression: str
    :param allow_self_connections: allow a neuron to connect to itself
    :type allow_self_connections: bool
    """
    __slots__ = []

    def __init__(
            self, index_expression, allow_self_connections=True, rng=None,
            safe=True, callback=None, verbose=False):
        # pylint: disable=too-many-arguments
        super(IndexBasedProbabilityConnector, self).__init__(
            index_expression=index_expression,
            allow_self_connections=allow_self_connections, rng=rng,
            safe=safe, callback=callback, verbose=verbose)
