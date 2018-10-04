from BreakOut.spinn_breakout.python_models.breakout import Breakout
from spynnaker8.utilities import DataHolder

_defs = Breakout.default_parameters

class BreakoutDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,
            WIDTH_PIXELS=_defs['width'],
            HEIGHT_PIXELS=_defs['height'],
            COLOUR_BITS=_defs['colour_bits'],
            constraints=_defs['constraints'],
            label=_defs['label'],
            incoming_spike_buffer_size=_defs['incoming_spike_buffer_size'],
            MAX_SIM_DURATION=_defs['duration']):
        # pylint: disable=too-many-arguments

        super(BreakoutDataHolder, self).__init__({
            'width': WIDTH_PIXELS,
            'height': HEIGHT_PIXELS,
            'colour_bits': COLOUR_BITS,
            'constraints': constraints,
            'label': label,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'simulation_duration_ms': MAX_SIM_DURATION
        })

    @staticmethod
    def build_model():
        return Breakout

