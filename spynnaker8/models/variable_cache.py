class VariableCache(object):
    """ Simple holder method to keep data, IDs, indexes and units together

    Typically used to recreate the neo object for one type of variable for\
    one segment
    """
    __slots__ = ("_data", "_indexes", "_n_neurons", "_units", "_sampling_interval")

    def __init__(self, data, indexes, n_neurons, units, sampling_interval):
        """
        :param data: raw data in spynakker format
        :type data: nparray
        :param indexes: Population indexes for which data was collected
        :type indexes: list (int)
        :param n_neurons: Number of neurons in the population.
            Regardless of if they where recording or not.
        :type n_neurons: int
        :param units: the units in which the data is
        :type units: str
        """
        self._data = data
        self._indexes = indexes
        self._n_neurons = n_neurons
        self._units = units
        self._sampling_interval = sampling_interval

    @property
    def data(self):
        return self._data

    @property
    def indexes(self):
        return self._indexes

    @property
    def n_neurons(self):
        return self._n_neurons

    @property
    def units(self):
        return self._units

    @property
    def sampling_interval(self):
        return self._sampling_interval
