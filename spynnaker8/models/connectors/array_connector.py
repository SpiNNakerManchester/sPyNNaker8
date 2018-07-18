from spynnaker.pyNN.models.neural_projections.connectors \
    import ArrayConnector as CommonArrayConnector


class ArrayConnector(CommonArrayConnector):
    """
    Create an array connector.

    :param array: an array of integers
    :type array: integer
    """
    __slots__ = []

    def __init__(
            self, array, safe=True, callback=None, verbose=False):
        # pylint: disable=too-many-arguments
        super(ArrayConnector, self).__init__(
            array=array,
            safe=safe, callback=callback, verbose=verbose)
