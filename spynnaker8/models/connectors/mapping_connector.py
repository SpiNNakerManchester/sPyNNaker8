from spynnaker.pyNN.models.neural_projections.connectors import (
    MappingConnector as
    CommonMappingConnector)


class MappingConnector(CommonMappingConnector):
    """
    Create a mapping connector.

    :param descriptions to follow, see sPyNNaker class
    """
    __slots__ = []

    def __init__(
            self, width, height, channel, height_bits, channel_bits=1,
            event_bits=0, safe=True, verbose=False):
        # pylint: disable=too-many-arguments
        super(MappingConnector, self).__init__(
            width, height, channel, height_bits, channel_bits,
            event_bits, safe=safe, verbose=verbose)
