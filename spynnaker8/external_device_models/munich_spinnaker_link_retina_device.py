from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import MunichRetinaDevice


class MunichRetinaDeviceDataHolder(DataHolder):
    def __init__(
            self, retina_key, spinnaker_link_id, position,
            label=MunichRetinaDevice.default_parameters['label'],
            polarity=MunichRetinaDevice.default_parameters['polarity'],
            board_address=MunichRetinaDevice.default_parameters[
                'board_address']):
        DataHolder.__init__(
            self, {
                'retina_key': retina_key,
                'spinnaker_link_id': spinnaker_link_id,
                'position': position, 'label': label, 'polarity': polarity,
                'board_address': board_address})

    @staticmethod
    def build_model():
        return MunichRetinaDevice
