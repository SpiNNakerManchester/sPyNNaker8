from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import ArbitraryFPGADevice


class ArbitraryFPGADeviceDataHolder(DataHolder):

    def __init__(
            self, fpga_link_id, fpga_id,
            board_address=ArbitraryFPGADevice.default_parameters[
                'board_address'],
            label=ArbitraryFPGADevice.default_parameters['label']):
        DataHolder.__init__(
            self, {'fpga_link_id': fpga_link_id, 'fpga_id': fpga_id,
                   'board_address': board_address, 'label': label})

    @staticmethod
    def build_model():
        return ArbitraryFPGADevice
