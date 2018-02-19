from unittest import SkipTest

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim

N_NEURONS = 5
LABEL = "pop_1"


class Test_IDMixin(BaseTestCase):

    def test_cells(self):
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(N_NEURONS, sim.IF_curr_exp(), label=LABEL)
        cells = pop_1.all_cells
        assert 0 == cells[0]._id
        assert pop_1 == cells[0]._population

    def test_get_set(self):
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(N_NEURONS, sim.IF_curr_exp(), label=LABEL)
        cells = pop_1.all_cells
        p_tau_m = pop_1.get("tau_m")
        tau_m_3 = cells[3].tau_m
        assert p_tau_m[3] == tau_m_3[0]
        cells[2].tau_m = 2
        p_tau_m = pop_1.get("tau_m")
        assert 2 == p_tau_m[2]
        parm = cells[1].get_parameters()
        assert True