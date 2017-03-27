from spynnaker.pyNN.models.neural_projections.connectors.\
    abstract_connector import AbstractConnector
from pyNN.connectors import IndexBasedProbabilityConnector as \
    PyNNIndexBasedProbabilityConnector

class IndexBasedProbabilityConnector(
        AbstractConnector, PyNNIndexBasedProbabilityConnector):

    def __init__(
            self, index_expression, allow_self_connections=True, rng=None,
            safe=True, callback=None):
        AbstractConnector.__init__(self, safe=safe)
        PyNNIndexBasedProbabilityConnector.__init__(
            self, index_expression=index_expression,
            allow_self_connections=allow_self_connections, rng=rng,
            safe=safe, callback=callback)
        raise NotImplementedError
