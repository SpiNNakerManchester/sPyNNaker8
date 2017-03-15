from neo import Block


class SpynnakerNeoBlock(Block):
    """ neo block that encapsulates the demands of PyNN in that it expects
    a parameter segments.
    """

    def __init__(
            self, name=None, description=None, file_origin=None,
            file_datetime=None, rec_datetime=None, index=None,
            **annotations):

        Block.__init__(
            self, name, description, file_origin, file_datetime, rec_datetime,
            index, **annotations)

        self._segments = list()

    @property
    def segments(self):
        return self._segments

    @segments.setter
    def segments(self, new_value):
        self._segments = new_value
