class DataHolder(object):
    def __init__(self, data_items):
        self._data_items = data_items

    def add_item(self, name, value):
        self._data_items[name] = value

    @property
    def data_items(self):
        return self._data_items

    @staticmethod
    def build_model():
        pass
