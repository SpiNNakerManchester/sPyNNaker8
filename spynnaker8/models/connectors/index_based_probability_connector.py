from spynnaker.pyNN.models.neural_projections.connectors import \
    IndexBasedProbabilityConnector as CommonIndexBasedProbabilityConnector
#from pyNN.connectors import IndexBasedProbabilityConnector as \
#    PyNNIndexBasedProbabilityConnector


class IndexBasedProbabilityConnector(CommonIndexBasedProbabilityConnector):

    def __init__(
            self, index_expression, allow_self_connections=True, rng=None,
            safe=True, callback=None, verbose=False):

        CommonIndexBasedProbabilityConnector.__init__(
            self, index_expression=index_expression,
            allow_self_connections=allow_self_connections, rng=rng,
            safe=safe, callback=callback, verbose=verbose)

