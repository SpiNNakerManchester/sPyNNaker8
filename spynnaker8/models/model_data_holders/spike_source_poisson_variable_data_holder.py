from spynnaker.pyNN.models.spike_source import SpikeSourcePoissonVariable
from spynnaker8.utilities import DataHolder

_np_defs = SpikeSourcePoissonVariable.non_pynn_default_parameters
_defs = SpikeSourcePoissonVariable.default_parameters


class SpikeSourcePoissonVariableDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,
            constraints=_np_defs['constraints'],
            label=_np_defs['label'],
            rates=_defs['rates'],
            starts=_defs['starts'],
            durations=_defs['durations'],
            seed=_np_defs['seed']):
        # pylint: disable=too-many-arguments
        super(SpikeSourcePoissonVariableDataHolder, self).__init__({
            'constraints': constraints, 'label': label, 'rates': rates,
            'starts': starts, 'durations': durations, 'seed': seed})

    @staticmethod
    def build_model():
        return SpikeSourcePoissonVariable
