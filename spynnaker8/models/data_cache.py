from datetime import datetime

class DataCache(object):

    _cache = dict()

    def __init__(self, segment_number, t):
        self._segment_number = segment_number
        self._t = t

    def has_data(self, variable):
        return variable in self._cache

    def get_data(self, variable):
        return self._cache[variable]

    def save_data(self, data, variable):
        self._rec_datetime = datetime.now()
        self._cache[variable] = data

    @property
    def rec_datetime(self):
        return self._rec_datetime

    @property
    def t(self):
        return self._t