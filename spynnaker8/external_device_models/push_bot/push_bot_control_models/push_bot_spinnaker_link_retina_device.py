from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_spinnaker_link \
    import PushBotSpiNNakerLinkRetinaDevice

_defaults = PushBotSpiNNakerLinkRetinaDevice.default_parameters


class PushBotSpinnakerLinkRetinaDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link_id, protocol, resolution,
            board_address=_defaults['board_address'],
            label=_defaults['label']):
        # pylint: disable=too-many-arguments
        super(PushBotSpinnakerLinkRetinaDeviceDataHolder, self).__init__({
            'board_address': board_address,
            'label': label,
            'protocol': protocol,
            'resolution': resolution,
            'spinnaker_link_id': spinnaker_link_id})

    @staticmethod
    def build_model():
        return PushBotSpiNNakerLinkRetinaDevice
