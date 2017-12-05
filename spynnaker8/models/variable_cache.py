class VariableCache(object):
    """
    Simple holder method to keep data, ids, indexes and units together

    Typically used to recreate the neo object for one type of variable for
    one segment
    """
    __slots__ = ("_data", "_ids", "_units", "_sampling_interval")

    def __init__(self, data, ids, units, sampling_interval):
        """

        :param data: raw data in spynakker format
        :type data: nparray
        :param ids: ids for which data should be returned
        :type nparray
        :param units: the units in which the data is
        :type units: str
        """
        self._data = data
        self._ids = ids
        self._units = units
        self._sampling_interval = sampling_interval

    @property
    def data(self):
        return self._data

    @property
    def ids(self):
        return self._ids

    @property
    def units(self):
        return self._units

    @property
    def sampling_interval(self):
        return self._sampling_interval
