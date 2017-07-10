class DataCache(object):

    _cache = dict()
    _record_times = dict()

    def has_data(self, variable, record_time):
        return variable in self._record_times

    def get_data(self, variable):
        return self._cache[variable]

    def save_data(self, data, variable,record_time):
        self._cache[variable] = data
        self._record_times[variable] = record_time
