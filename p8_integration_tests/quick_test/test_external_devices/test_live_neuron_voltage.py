# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase
from spynnaker.pyNN.external_devices_models import AbstractEthernetTranslator
from spynnaker.pyNN.external_devices_models\
    .abstract_multicast_controllable_device import (
        AbstractMulticastControllableDevice, SendType)
from data_specification.enums.data_type import DataType
import decimal
import numpy


class Translator(AbstractEthernetTranslator):

    def __init__(self):
        self.voltages = list()

    def translate_control_packet(self, multicast_packet):
        voltage = multicast_packet.payload
        self.voltages.append(
            (float)(decimal.Decimal(voltage) / DataType.S1615.scale))


class Device(AbstractMulticastControllableDevice):

    @property
    def device_control_key(self):
        return 0

    @property
    def device_control_max_value(self):
        return DataType.S1615.max

    @property
    def device_control_min_value(self):
        return DataType.S1615.min

    @property
    def device_control_partition_id(self):
        return "DEVICE_CONTROL"

    @property
    def device_control_scaling_factor(self):
        return 1.0

    @property
    def device_control_send_type(self):
        return SendType.SEND_TYPE_ACCUM

    @property
    def device_control_timesteps_between_sending(self):
        return 10

    @property
    def device_control_uses_payload(self):
        return True


def live_neuron_voltage():
    p.setup(1.0)
    run_time = 1000.0
    translator = Translator()
    devices = [Device()]
    create_edges = False
    stim = p.Population(1, p.SpikeSourceArray(range(0, 1000, 100)))
    model = p.external_devices.ExternalDeviceLifControl(
        devices, create_edges, translator)
    ext_pop = p.external_devices.EthernetControlPopulation(1, model)
    ext_pop.record(["v"])
    p.Projection(
        stim, ext_pop, p.OneToOneConnector(), p.StaticSynapse(1.0, 1.0))
    p.run(run_time)
    v = ext_pop.get_data("v").segments[0].analogsignals[0].as_array()[:, 0]
    p.end()
    assert(
        len(translator.voltages) ==
        run_time // devices[0].device_control_timesteps_between_sending)
    relevant_v = v[
        1:1000:devices[0].device_control_timesteps_between_sending]
    print(v)
    print(relevant_v)
    print(translator.voltages)
    assert(numpy.array_equal(relevant_v, translator.voltages))


class TestLiveNeuronVoltage(BaseTestCase):

    def test_live_neuron_voltage(self):
        self.runsafe(live_neuron_voltage)


if __name__ == '__main__':
    live_neuron_voltage()
