from spynnaker.pyNN.models.neural_projections.connectors.\
    abstract_connector import \
    AbstractConnector
from pyNN.connectors import ArrayConnector as PyNNArrayConnector


class ArrayConnector(AbstractConnector, PyNNArrayConnector):

    def __init__(self, array, safe=True, callback=None):
        AbstractConnector.__init__(self, safe=safe)
        PyNNArrayConnector.__init__(
            self, array=array, safe=safe, callback=callback)
        raise NotImplementedError
