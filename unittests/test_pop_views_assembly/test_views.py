import pytest

from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim
from spynnaker8.models.populations.population_view import PopulationView

class Test_IDMixin(BaseTestCase):

    def test_simple(self):
        n_neurons = 5
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        mask = [1, 3]
        view = PopulationView(pop_1, mask, label=label)
        self.assertEqual(2, view.size)
        self.assertEqual(label, view.label)
        self.assertEqual(pop_1.celltype, view.celltype)

        view_initial_values = view.initial_values
        pop_initial_values = pop_1.initial_values
        self.assertEqual(len(view_initial_values), len(pop_initial_values))
        for key in pop_initial_values:
            self.assertEqual(
                pop_initial_values[key][3], view_initial_values[key][1])

        self.assertEqual(pop_1, view.parent)
        self.assertEqual(mask, view.mask)

        cells = view.all_cells
        self.assertEqual(2, len(cells))
        self.assertEqual(1, cells[0].id)
        self.assertEqual(3, cells[1].id)

        self.assertEqual(cells, view.local_cells)
        self.assertEqual(cells[0], view[1])

        iterator = iter(view)
        self.assertEqual(1, iterator.next().id)
        self.assertEqual(3, iterator.next().id)
        with pytest.raises(StopIteration):
            iterator.next()

        self.assertEqual(2, len(view))

        iterator = view.all()
        self.assertEqual(1, iterator.next().id)
        self.assertEqual(3, iterator.next().id)
        with pytest.raises(StopIteration):
            iterator.next()

        self.assertEqual(view.can_record("v"), pop_1.can_record("v"))
        self.assertEqual(view.conductance_based, pop_1.conductance_based)

        describe = view.describe()
        self.assertIn('PopulationView "pop_1"', describe)
        self.assertIn('parent : "pop_1"', describe)
        self.assertIn('size   : 2', describe)
        self.assertIn('mask   : [1, 3]', describe)

        self.assertEqual(pop_1.find_units("v"), view.find_units("v"))

        sim.end()


    def test_depricated_not_implemented(self):
        n_neurons = 5
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        view = PopulationView(pop_1, [1, 3], label="Odds")
        with pytest.raises(NotImplementedError):
            view.getSpikes("a_args")
        with pytest.raises(NotImplementedError):
            view.getSpikes(a_kargs="foo")
        view.getSpikes()
        sim.end()


    def test_get_set(self):
        n_neurons = 4
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        view = PopulationView(pop_1, [1, 3], label="Odds")

        pop_1.set(tau_m=2)
        self.assertEqual([2, 2, 2, 2], pop_1.get("tau_m"))
        self.assertEqual([2, 2], view.get("tau_m"))
        view.set(tau_m=3)
        self.assertEqual([2, 3, 2, 3], pop_1.get("tau_m"))
        sim.end()
