from spynnaker.pyNN.models.neural_projections.connectors.from_file_connector \
    import FromFileConnector as CommonFromFileConnector

from pyNN.connectors import FromFileConnector as PyNNFromFileConnector


class FromFileConnector(CommonFromFileConnector, PyNNFromFileConnector):
    def __init__(
            self, file, callback=None,  # @ReservedAssignment
            distributed=False, safe=True, verbose=False):
        CommonFromFileConnector.__init__(
            self, file=None, distributed=distributed, safe=safe,
            verbose=verbose)
        PyNNFromFileConnector.__init__(
            self, file=file, distributed=distributed, safe=safe,
            callback=callback)
