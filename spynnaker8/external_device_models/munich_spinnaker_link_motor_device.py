from spynnaker8.utilities import DataHolder
from spynnaker.pyNN.external_devices_models import MunichMotorDevice


class MunichMotorDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link_id,
            board_address=MunichMotorDevice.default_parameters[
                'board_address'],
            speed=MunichMotorDevice.default_parameters['speed'],
            sample_time=MunichMotorDevice.default_parameters['sample_time'],
            update_time=MunichMotorDevice.default_parameters['update_time'],
            delay_time=MunichMotorDevice.default_parameters['delay_time'],
            delta_threshold=MunichMotorDevice.default_parameters[
                'delta_threshold'],
            continue_if_not_different=MunichMotorDevice.default_parameters[
                'continue_if_not_different'],
            label=MunichMotorDevice.default_parameters['label']):

        DataHolder.__init__(
            self, {
                'spinnaker_link_id': spinnaker_link_id,
                'board_address': board_address, 'label': label,
                'speed': speed, 'sample_time': sample_time,
                'update_time': update_time, 'delay_time': delay_time,
                'delta_threshold': delta_threshold,
                'continue_if_not_different': continue_if_not_different})

    @staticmethod
    def build_model():
        return MunichMotorDevice
