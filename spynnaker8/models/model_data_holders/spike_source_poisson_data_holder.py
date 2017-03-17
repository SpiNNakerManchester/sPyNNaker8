from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson
from spynnaker8.utilities.data_holder import DataHolder


class SpikeSourcePoissonDataHolder(DataHolder):
    def __init__(
            self,
            constraints=SpikeSourcePoisson.none_pynn_default_parameters[
                'constraints'],
            label=SpikeSourcePoisson.none_pynn_default_parameters['label'],
            rate=SpikeSourcePoisson.default_parameters['rate'],
            start=SpikeSourcePoisson.default_parameters['start'],
            duration=SpikeSourcePoisson.default_parameters['duration'],
            seed=SpikeSourcePoisson.none_pynn_default_parameters['seed']):
        DataHolder.__init__(
            self, {'constraints': constraints, 'label': label, 'rate': rate,
                   'start': start, 'duration': duration, 'seed': seed})

    @staticmethod
    def build_model():
        return SpikeSourcePoisson
