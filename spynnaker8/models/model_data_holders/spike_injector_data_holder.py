from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.models.utility_models import SpikeInjector

_defaults = SpikeInjector.default_parameters


class SpikeInjectorDataHolder(DataHolder):

    def __init__(
            self, label=_defaults['label'], port=_defaults['port'],
            virtual_key=_defaults['virtual_key']):
        super(SpikeInjectorDataHolder, self).__init__({
            'label': label, 'port': port, 'virtual_key': virtual_key})

    @staticmethod
    def build_model():
        return SpikeInjector
