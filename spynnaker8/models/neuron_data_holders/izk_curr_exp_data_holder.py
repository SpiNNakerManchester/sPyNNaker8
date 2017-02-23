from spynnaker8.utilities.data_holder import DataHolder
from spynnaker8.models.builds.izk_curr_exp import IzkCurrExp


class IzkCurrExpDataHolder(DataHolder):
    def __init__(self, data_items):
        DataHolder.__init__(self, data_items)

    @staticmethod
    def build_model():
        return IzkCurrExp
