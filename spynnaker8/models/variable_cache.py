class VariableCache(object):
    """
    Simple holder method to keep data, ids, indexes and units together

    Typically used to recreate the neo object for one type of variable for
    one segment
    """
    __slots__ = ("_data", "_ids", "_indexes", "_units")

    def __init__(self, data, ids, indexes, units):
        """

        :param data: raw data in spynakker format
        :type data: nparray
        :param ids: ids for which data should be returned
        :type nparray
        :param indexes: indexes for whcih data should be retreived
        :type indexes: nparray
        :param units: the units in which the data is
        :type units: str
        """
        self._data = data
        self._ids = ids
        self._indexes = indexes
        self._units = units

    @property
    def data(self):
        return self._data

    @property
    def ids(self):
        return self._ids

    @property
    def indexes(self):
        return self._indexes

    @property
    def units(self):
        return self._units
