from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import ExternalCochleaDevice


class ExternalCochleaDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link,
            label=ExternalCochleaDevice.default_parameters['label'],
            board_address=ExternalCochleaDevice.default_parameters[
                'board_address']):
        super(ExternalCochleaDeviceDataHolder, self).__init__({
            'board_address': board_address,
            'label': label,
            'spinnaker_link': spinnaker_link})

    @staticmethod
    def build_model():
        return ExternalCochleaDevice
