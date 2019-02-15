from spynnaker.pyNN.models.neural_projections.connectors import (
    CSAConnector as
    CommonCSAConnector)


class CSAConnector(CommonCSAConnector):
    """
    Create an CSA (Connection Set Algebra, Djurfeldt 2012) connector.

    :param cset: a connection set description
    :type cset: string
    """
    __slots__ = []

    def __init__(
            self, cset, safe=True, callback=None, verbose=False):
        # pylint: disable=too-many-arguments
        super(CSAConnector, self).__init__(
            cset=cset,
            safe=safe, callback=callback, verbose=verbose)
