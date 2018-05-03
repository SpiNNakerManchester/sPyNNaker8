from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase, abstractmethod


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


@add_metaclass(AbstractBase)
class DataHolder(object):
    """ Holds descriptions of the parameters to a model. Allows the model\
        instance parameters to be updated.
    """

    __slots__ = [
        "_data_items"]

    def __init__(self, data_items):
        """
        :param data_items: The initial configurations of the parameters.
        :type data_items: dict(str,object)
        """
        self._data_items = data_items

    def add_item(self, name, value):
        """ Add (or update) a parameter of the model.

        :param name: The name of the parameter
        :type name: str
        :param value: The new value of the parameter
        """
        self._data_items[name] = value

    @property
    def data_items(self):
        """ Get the current parameters of the model.
        """
        return self._data_items

    @staticmethod
    @abstractmethod
    def build_model():
        """ Get the underlying concrete model that this class is holding\
            parameters for.
        """
        pass

    @ClassProperty
    @classmethod
    def default_parameters(cls):
        # print(cls)
        return cls.build_model().default_parameters

    # Ugly hack because of stack of interacting decorators
    default_parameters.__doc__ = """
        Get the default values for the parameters of the model.

        :rtype: dict(str,object)
        """

    @classmethod
    def get_parameter_names(cls):
        """ Get the names of the parameters of the model.

        :rtype: iterable(str)
        """
        return cls.default_parameters.keys()
