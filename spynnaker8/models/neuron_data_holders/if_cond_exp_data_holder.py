from spynnaker8.utilities.data_holder import DataHolder
from spynnaker8.models.builds.if_cond_exp import IFCondExp


class IFCondExpDataHolder(DataHolder):
    def __init__(self, data_items):
        DataHolder.__init__(self, data_items)

    @staticmethod
    def build_model():
        return IFCondExp
