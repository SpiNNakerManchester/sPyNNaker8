class VariableCache(object):
    """ Simple holder method to keep data, IDs, indexes and units together

    Typically used to recreate the neo object for one type of variable for\
    one segment
    """
    __slots__ = ("_data", "_ids", "_units")

    def __init__(self, data, ids, units):
        """
        :param data: raw data in spynakker format
        :type data: nparray
        :param ids: ids for which data should be returned
        :type ids: nparray
        :param units: the units in which the data is
        :type units: str
        """
        self._data = data
        self._ids = ids
        self._units = units

    @property
    def data(self):
        return self._data

    @property
    def ids(self):
        return self._ids

    @property
    def units(self):
        return self._units
