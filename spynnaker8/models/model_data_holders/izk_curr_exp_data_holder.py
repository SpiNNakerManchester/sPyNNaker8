from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base \
    import IzkCurrExpBase


class IzkCurrExpDataHolder(DataHolder):
    def __init__(self, data_items):
        DataHolder.__init__(self, data_items)

    @staticmethod
    def build_model():
        return IzkCurrExpBase
