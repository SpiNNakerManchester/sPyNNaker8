from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import ExternalFPGARetinaDevice


class ExternalFPGARetinaDeviceDataHolder(DataHolder):

    MODE_128 = ExternalFPGARetinaDevice.MODE_128
    MODE_64 = ExternalFPGARetinaDevice.MODE_64
    MODE_32 = ExternalFPGARetinaDevice.MODE_32
    MODE_16 = ExternalFPGARetinaDevice.MODE_16
    UP_POLARITY = ExternalFPGARetinaDevice.UP_POLARITY
    DOWN_POLARITY = ExternalFPGARetinaDevice.DOWN_POLARITY
    MERGED_POLARITY = ExternalFPGARetinaDevice.MERGED_POLARITY

    def __init__(
            self, mode, retina_key, spinnaker_link_id, polarity,
            label=ExternalFPGARetinaDevice.default_parameters['label'],
            board_address=ExternalFPGARetinaDevice.default_parameters[
                'board_address']):
        DataHolder.__init__(
            self, {'spinnaker_link_id': spinnaker_link_id, 'mode': mode,
                   'board_address': board_address, 'label': label,
                   'retina_key': retina_key, 'polarity': polarity})

    @staticmethod
    def build_model():
        return ExternalFPGARetinaDevice

    def get_n_neurons(self):
        return ExternalFPGARetinaDevice.get_n_neurons(
            self._data_items['mode'], self._data_items['polarity'])
