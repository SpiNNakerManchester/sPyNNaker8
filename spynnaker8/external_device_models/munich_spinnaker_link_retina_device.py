from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import MunichRetinaDevice


class MunichRetinaDeviceDataHolder(DataHolder):
    def __init__(
            self, retina_key, spinnaker_link_id, position,
            label=MunichRetinaDevice.default_parameters['label'],
            polarity=MunichRetinaDevice.default_parameters['polarity'],
            board_address=MunichRetinaDevice.default_parameters[
                'board_address']):
        # pylint: disable=too-many-arguments
        super(MunichRetinaDeviceDataHolder, self).__init__({
            'board_address': board_address,
            'label': label,
            'polarity': polarity,
            'position': position,
            'retina_key': retina_key,
            'spinnaker_link_id': spinnaker_link_id})

    @staticmethod
    def build_model():
        return MunichRetinaDevice
