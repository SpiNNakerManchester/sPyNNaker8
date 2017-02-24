from spynnaker8.utilities.data_holder import DataHolder
from spynnaker.pyNN.models.neuron.builds.izk_cond_exp_base import \
    IzkCondExpBase


class IzkCondExpDataHolder(DataHolder):
    def __init__(self, data_items):
        DataHolder.__init__(self, data_items)

    @staticmethod
    def build_model():
        return IzkCondExpBase
