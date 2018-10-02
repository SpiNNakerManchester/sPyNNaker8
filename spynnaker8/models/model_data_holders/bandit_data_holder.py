from bandit.spinn_bandit import Bandit
from spynnaker8.utilities import DataHolder

_defs = Bandit.default_parameters


class BanditDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,
            arms=_defs['arms'],
            reward_delay=_defs['reward_delay'],
            constraints=_defs['constraints'],
            label=_defs['label'],
            incoming_spike_buffer_size=_defs['incoming_spike_buffer_size'],
            simulation_duration_ms=_defs['duration']):
        # pylint: disable=too-many-arguments

        super(BanditDataHolder, self).__init__({
            'arms': arms, 'reward_delay': reward_delay,
            'constraints': constraints, 'label': label, 'incoming_spike_buffer_size':incoming_spike_buffer_size,
            'simulation_duration_ms': simulation_duration_ms})

    @staticmethod
    def build_model():
        return Bandit