from spynnaker.pyNN.models.spike_source import SpikeSourcePoisson
from spynnaker8.utilities import DataHolder

_np_defs = SpikeSourcePoisson.non_pynn_default_parameters
_defs = SpikeSourcePoisson.default_parameters


class SpikeSourcePoissonDataHolder(DataHolder):
    __slots__ = []

    def __init__(
            self,
            constraints=_np_defs['constraints'],
            label=_np_defs['label'],
            rate=_defs['rate'],
            start=_defs['start'],
            duration=_defs['duration'],
            seed=_np_defs['seed']):
        # pylint: disable=too-many-arguments
        super(SpikeSourcePoissonDataHolder, self).__init__({
            'constraints': constraints, 'label': label, 'rate': rate,
            'start': start, 'duration': duration, 'seed': seed})

    @staticmethod
    def build_model():
        return SpikeSourcePoisson
