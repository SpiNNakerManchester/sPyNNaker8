from spinn_front_end_common.utilities.exceptions import ConfigurationException


class Spynnaker8Exception(Exception):
    """ Superclass of all exceptions from the pynn module
    """


class MemReadException(Spynnaker8Exception):
    """ Raised when the pynn front end fails to read a certain memory region
    """
    pass


class FilterableException(Spynnaker8Exception):
    """ Raised when it is not possible to determine if an edge should be\
        filtered
    """
    pass


class SynapticConfigurationException(ConfigurationException):
    """ Raised when the synaptic manager fails for some reason
    """
    pass


class SynapticBlockGenerationException(ConfigurationException):
    """ Raised when the synaptic manager fails to generate a synaptic block
    """
    pass


class SynapticBlockReadException(ConfigurationException):
    """ Raised when the synaptic manager fails to read a synaptic block or\
        convert it into readable values
    """
    pass


class SynapticMaxIncomingAtomsSupportException(ConfigurationException):
    """ Raised when a synaptic sublist exceeds the max atoms possible to be\
        supported
    """
    pass


class DelayExtensionException(ConfigurationException):
    """ Raised when a delay extension vertex fails
    """
    pass


class InvalidParameterType(Spynnaker8Exception):
    """ Raised when a parameter is not recognised
    """
    pass
