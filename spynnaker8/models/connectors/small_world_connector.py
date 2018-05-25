from pyNN.space import Space

from spynnaker.pyNN.models.neural_projections.connectors \
    import SmallWorldConnector as _BaseClass


class SmallWorldConnector(_BaseClass):
    __slots__ = []

    def __init__(
            self, degree, rewiring, allow_self_connections=True, space=Space(),
            safe=True, verbose=False, n_connections=None):
        # pylint: disable=too-many-arguments
        super(SmallWorldConnector, self).__init__(
            degree=degree, rewiring=rewiring,
            allow_self_connections=allow_self_connections,
            safe=safe, verbose=verbose, n_connections=n_connections)
