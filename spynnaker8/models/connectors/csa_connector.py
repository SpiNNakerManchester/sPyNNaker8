from spynnaker.pyNN.models.neural_projections.connectors \
    import CSAConnector as CommonCSAConnector


class CSAConnector(CommonCSAConnector):
    """
    Create an CSA (Connection Set Algebra, Djurfeldt 2012) connector.

    :param csa: a csa description of the connections
    :type csa: string
    """
    __slots__ = []

    def __init__(
            self, csa, safe=True, callback=None, verbose=False):
        # pylint: disable=too-many-arguments
        super(CSAConnector, self).__init__(
            array=csa,
            safe=safe, callback=callback, verbose=verbose)
