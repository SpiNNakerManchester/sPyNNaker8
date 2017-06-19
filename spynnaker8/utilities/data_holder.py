from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase, abstractmethod


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


@add_metaclass(AbstractBase)
class DataHolder(object):
    def __init__(self, data_items):
        self._data_items = data_items

    def add_item(self, name, value):
        self._data_items[name] = value

    @property
    def data_items(self):
        return self._data_items

    @staticmethod
    @abstractmethod
    def build_model():
        pass

    @ClassProperty
    @classmethod
    def default_parameters(cls):
        print cls
        return cls.build_model().default_parameters

    @classmethod
    def get_parameter_names(cls):
        return cls.default_parameters.keys()
