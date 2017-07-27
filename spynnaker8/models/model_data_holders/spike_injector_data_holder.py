from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.utility_models import SpikeInjector


class SpikeInjectorDataHolder(DataHolder):

    def __init__(
            self, label=SpikeInjector.default_parameters['label'],
            port=SpikeInjector.default_parameters['port'],
            virtual_key=SpikeInjector.default_parameters['virtual_key']):
        DataHolder.__init__(
            self, {'label': label, 'port': port, 'virtual_key': virtual_key})

    @staticmethod
    def build_model():
        return SpikeInjector
