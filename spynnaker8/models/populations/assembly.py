from pyNN import common as pynn_common
from spinn_front_end_common.utilities import globals_variables


class Assembly(pynn_common.Assembly):

    @property
    def _simulator(self):
        return globals_variables.get_simulator()
