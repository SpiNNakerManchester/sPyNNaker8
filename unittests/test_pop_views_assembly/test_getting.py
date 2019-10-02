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

from __future__ import division
import pickle
from unittest import SkipTest
import numpy
import pytest
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities.globals_variables import get_simulator
import spynnaker8 as sim
from spynnaker8.utilities import neo_convertor
from p8_integration_tests.base_test_case import BaseTestCase


def mock_spikes():
    return numpy.array(
        [[0, 7], [0, 20], [0, 24], [0, 34], [0, 53], [0, 67], [0, 77],
         [1, 8], [1, 20], [1, 53],
         [2, 45], [2, 76]])


def mock_v_all(variable):
    indexes = [0, 1, 2, 3]
    data = numpy.empty((100, 4))
    for i in range(100):
        for j in indexes:
            data[i][j] = -65 + j + i/100
    sampling_interval = 1
    return (data, indexes, sampling_interval)


def mock_v_one_two(variable):
    indexes = [1, 2]
    data = numpy.empty((100, 2))
    for i in range(100):
        for j in range(len(indexes)):
            data[i][j] = -65 + indexes[j] + i/100
    sampling_interval = 1
    return (data, indexes, sampling_interval)


def mock_time():
    return 100


def trim_spikes(spikes, indexes):
    return [[n, t] for [n, t] in spikes if n in indexes]


class TestGetting(BaseTestCase):

    def test_get_v_view(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp(), label="a label")
        pop.record("spikes")
        pop._get_spikes = mock_spikes
        pop._get_recorded_matrix = mock_v_all
        get_simulator().get_current_time = mock_time

        view = pop[1:3]
        neo = view.get_data("v")
        v = neo.segments[0].filter(name='v')[0].magnitude
        (target, _, _) = mock_v_one_two("v")
        assert v.shape == target.shape
        assert numpy.array_equal(v,  target)

        sim.end()

    def test_get_v_missing(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp(), label="a label")
        pop._get_recorded_matrix = mock_v_one_two
        get_simulator().get_current_time = mock_time

        view = pop[0:3]
        neo = view.get_data("v")
        v = neo.segments[0].filter(name='v')[0].magnitude
        (target, _, _) = mock_v_one_two("v")
        assert numpy.array_equal(
            [1, 2], neo.segments[0].filter(name='v')[0].channel_index.index)
        assert v.shape == target.shape
        assert numpy.array_equal(v,  target)

        sim.end()

    def test_get_spike_counts(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp(), label="a label")
        pop.record("spikes")

        assert {0: 0, 1: 0, 2: 0, 3: 0} == pop.get_spike_counts()

        view = pop[1:4]
        assert {1: 0, 2: 0, 3: 0} == view.get_spike_counts()

        sim.end()

    def test_get_(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(4, sim.IF_curr_exp(), label="a label")
        pop._get_spikes = mock_spikes
        pop._get_recorded_matrix = mock_v_all
        get_simulator().get_current_time = mock_time

        v = pop.spinnaker_get_data("v")
        assert 400 == len(v)

        v = pop.spinnaker_get_data(["v"])
        assert 400 == len(v)

        with pytest.raises(ConfigurationException):
            pop.spinnaker_get_data(["v", "spikes"])
        sim.end()
