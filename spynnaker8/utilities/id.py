from pyNN import common as PyNNCommon


class ID(int, PyNNCommon.IDMixin):
    """ some filter container for allowing rnadom setters of values

    """

    def __init__(self, n):
        """Create an ID object with numerical value `n`."""
        int.__init__(n)
        PyNNCommon.IDMixin.__init__(self)
