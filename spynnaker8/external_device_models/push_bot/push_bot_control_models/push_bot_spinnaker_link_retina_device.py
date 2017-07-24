from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models.push_bot.push_bot_spinnaker_link \
    import PushBotSpiNNakerLinkRetinaDevice


class PushBotSpinnakerLinkRetinaDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link_id, protocol, resolution,
            board_address=PushBotSpiNNakerLinkRetinaDevice.
            default_parameters['board_address'],
            label=PushBotSpiNNakerLinkRetinaDevice.
            default_parameters['label']):

        DataHolder.__init__(
            self, data_items={
                'spinnaker_link_id': spinnaker_link_id,
                'protocol': protocol,
                'resolution': resolution,
                'board_address': board_address,
                'label': label
            })

    @staticmethod
    def build_model():
        return PushBotSpiNNakerLinkRetinaDevice
