from unittest import SkipTest

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim

N_NEURONS = 4
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
        params = cells[1].get_parameters()
        p_i_offset = pop_1.get("i_offset")
        assert params["i_offset"][0] == p_i_offset[1]
        cells[2].set_parameters(tau_m=3, i_offset=13)
        params = cells[2].get_parameters()
        assert 13 == params["i_offset"][0]

    def test_is_local(self):
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(N_NEURONS, sim.IF_curr_exp(), label=LABEL)
        cells = pop_1.all_cells
        assert pop_1.is_local(2) == cells[2].local

    """
    def test_positions(self):
        grid_structure = sim.Grid2D(dx=1.0, dy=1.0, x0=0.0, y0=0.0)
        positions = grid_structure.generate_positions(4)
        pos_T = positions.T
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(N_NEURONS, sim.IF_curr_exp(), label=LABEL)
        cells = pop_1.all_cells
        assert "q" == pop_1.position[1]
    """
