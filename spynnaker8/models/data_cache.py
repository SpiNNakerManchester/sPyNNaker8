from datetime import datetime

from spynnaker8.models.variable_cache import VariableCache


class DataCache(object):
    """ Storage object to hold all the data to (re)create a Neo Segment

    Required because deepcopy does not work on neo Objects

    Stores the Data shared by all variable types at the top level
    and holds a cache for the variable specific data
    """

    __slots__ = ("_cache",
                 "_description",
                 "_first_id",
                 "_label",
                 "_rec_datetime",
                 "_recording_start_time",
                 "_sampling_interval",
                 "_segment_number",
                 "_t")

    _cache = dict()

    def __init__(self, label, description, segment_number,
                 recording_start_time, t, sampling_interval, first_id):
        """ constructor

        :param label: cache label
        :param description: cache description
        :param segment_number: cache segment number
        :param recording_start_time: when this cache was started in\
            recording space.
        :param t: time
        :param sampling_interval: sampling interval, same as t in spynnaker \
            world to date.
        :param first_id: first atom
        """
        self._label = label
        self._description = description
        self._segment_number = segment_number
        self._recording_start_time = recording_start_time
        self._t = t
        self._sampling_interval = sampling_interval
        self._first_id = first_id

    @property
    def variables(self):
        """Provides a list of which variables data has been cached for
        rtype: Iterator (str)
        """
        return self._cache.keys()

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @property
    def segment_number(self):
        return self._segment_number

    @property
    def recording_start_time(self):
        return self._recording_start_time

    @property
    def t(self):
        return self._t

    @property
    def sampling_interval(self):
        return self._sampling_interval

    @property
    def first_id(self):
        return self._first_id

    @property
    def rec_datetime(self):
        return self._rec_datetime

    def has_data(self, variable):
        """
        Checks if data for a variable has been cached

        :param variable: Name of variable
        :type variable: str
        :return: True if there is cached data
        :rtype bool
        """
        return variable in self._cache

    def get_data(self, variable):
        """
        Get the varaaible cahe for the named variable
        :param variable: name of variable to get cache for
        :rtype variable: str
        :return: The cache data, ids, indexes and units
        :rtype VariableCache
        """
        return self._cache[variable]

    def save_data(self, variable, data, ids, indexes, units):
        """
        Saves the data for one variable in this segment
        :param variable: name of variable data applies to
        :type variable: str
        :param data: raw data in spynakker format
        :type data: nparray
        :param ids: ids for which data should be returned
        :type nparray
        :param indexes: indexes for whcih data should be retreived
        :type indexes: nparray
        :param units: the units in which the data is
        :type units: str
        :rtype None
        """
        self._rec_datetime = datetime.now()
        variable_cache = VariableCache(data, ids, indexes, units)
        self._cache[variable] = variable_cache
