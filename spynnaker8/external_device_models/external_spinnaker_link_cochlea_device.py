from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import ExternalCochleaDevice


class ExternalCochleaDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link,
            label=ExternalCochleaDevice.default_parameters['label'],
            board_address=ExternalCochleaDevice.default_parameters[
                'board_address']):
        DataHolder.__init__(
            self, {'spinnaker_link': spinnaker_link,
                   'board_address': board_address, 'label': label})

    @staticmethod
    def build_model():
        print ("this is a very long line to intentionally break flake 8. blah blah blah")
        return ExternalCochleaDevice
