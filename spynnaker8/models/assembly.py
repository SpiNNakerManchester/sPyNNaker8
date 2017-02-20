from spynnaker8.utilities import globals_variables

from pyNN import common as pynn_common


class Assembly(pynn_common.Assembly):
    _simulator = globals_variables.get_simulator()
