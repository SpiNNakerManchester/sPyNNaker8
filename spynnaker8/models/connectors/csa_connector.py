from spynnaker.pyNN.models.neural_projections.connectors.\
    abstract_connector import AbstractConnector
from pyNN.connectors import CSAConnector as PyNNCSAConnector


class CSAConnector(AbstractConnector, PyNNCSAConnector):

    def __init__(self, cset, safe=True, callback=None):
        AbstractConnector.__init__(self, safe=safe)
        PyNNCSAConnector.__init__(
            self, cset=cset, safe=safe, callback=callback)
        raise NotImplementedError