class VariableCache(object):
    """ Simple holder method to keep data, IDs, indexes and units together

    Typically used to recreate the neo object for one type of variable for\
    one segment
    """
    __slots__ = ("_data", "_indexes", "_units", "_sampling_interval")

    def __init__(self, data, indexes, units, sampling_interval):
        """
        :param data: raw data in spynakker format
        :type data: nparray
        :param indexes: Population indexes for which data should be returned
        :type nparray
        :param units: the units in which the data is
        :type units: str
        """
        self._data = data
        self._indexes = indexes
        self._units = units
        self._sampling_interval = sampling_interval

    @property
    def data(self):
        return self._data

    @property
    def indexes(self):
        return self._indexes

    @property
    def units(self):
        return self._units

    @property
    def sampling_interval(self):
        return self._sampling_interval
