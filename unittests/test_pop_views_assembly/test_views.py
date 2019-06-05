import pytest
from pyNN.random import RandomDistribution, NumpyRNG
from spinn_front_end_common.utilities.exceptions import ConfigurationException
import spynnaker8 as sim
from spynnaker8.models.populations import PopulationView
from p8_integration_tests.base_test_case import BaseTestCase


class Test_IDMixin(BaseTestCase):

    def test_simple(self):
        n_neurons = 5
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        mask = [1, 3]
        view = PopulationView(pop_1, mask, label=label)
        self.assertEquals(2, view.size)
        self.assertEquals(2, view.local_size)

        self.assertEquals(label, view.label)
        self.assertEquals(pop_1.celltype, view.celltype)

        view_initial_values = view.initial_values
        pop_initial_values = pop_1.initial_values
        self.assertEquals(len(view_initial_values), len(pop_initial_values))
        for key in pop_initial_values:
            self.assertEquals(
                pop_initial_values[key][3], view_initial_values[key][1])

        self.assertEquals(pop_1, view.parent)
        self.assertEquals(mask, view.mask)

        cells = view.all_cells
        self.assertEquals(2, len(cells))
        self.assertEquals(1, cells[0].id)
        self.assertEquals(3, cells[1].id)

        self.assertEquals(cells, view.local_cells)
        self.assertEquals(cells[0], view[1])

        iterator = iter(view)
        self.assertEquals(1, next(iterator).id)
        self.assertEquals(3, next(iterator).id)
        with pytest.raises(StopIteration):
            next(iterator)

        self.assertEquals(2, len(view))

        iterator = view.all()
        self.assertEquals(1, next(iterator).id)
        self.assertEquals(3, next(iterator).id)
        with pytest.raises(StopIteration):
            next(iterator)

        self.assertEquals(view.can_record("v"), pop_1.can_record("v"))
        self.assertEquals(view.conductance_based, pop_1.conductance_based)

        describe = view.describe()
        self.assertIn('PopulationView "pop_1"', describe)
        self.assertIn('parent : "pop_1"', describe)
        self.assertIn('size   : 2', describe)
        self.assertIn('mask   : [1, 3]', describe)

        self.assertEquals(pop_1.find_units("v"), view.find_units("v"))

        sim.end()

    def test_get_set(self):
        n_neurons = 4
        label = "pop_1"
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label=label)
        view = PopulationView(pop_1, [1, 3], label="Odds")

        pop_1.set(tau_m=2)
        self.assertEquals([2, 2, 2, 2], pop_1.get("tau_m"))
        self.assertEquals([2, 2], view.get("tau_m", simplify=False))
        view.set(tau_m=3)
        self.assertEquals([2, 3, 2, 3], pop_1.get("tau_m"))
        sim.end()

    def test_view_of_view(self):
        n_neurons = 10
        sim.setup(timestep=1.0)
        pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
        view1 = PopulationView(pop_1, [1, 3, 5, 7, 9], label="Odds")
        view2 = PopulationView(view1, [1, 3], label="AlternativeOdds")
        # Not a normal way to access but good to test
        self.assertEquals([3, 7], view2._indexes)
        self.assertEquals(view2.parent, view1)
        self.assertEquals(view1.grandparent, pop_1)
        self.assertEquals(view2.grandparent, pop_1)
        cells = view2.all_cells
        self.assertEquals(3, cells[0].id)
        self.assertEquals(7, cells[1].id)
        self.assertEquals(3, view1.id_to_index(7))
        self.assertEquals([3, 0], view1.id_to_index([7, 1]))
        self.assertEquals(1, view2.id_to_index(7))
        view3 = view1[1:3]
        self.assertEquals([3, 5], view3._indexes)
        view4 = view1.sample(2)
        self.assertEquals(2, len(view4._indexes))
        sim.end()

    def test_initial_value(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(5, sim.IF_curr_exp(), label="pop_1")
        self.assertEquals([-65, -65, -65, -65, -65], pop.get_initial_value("v"))
        view = PopulationView(pop, [1, 3], label="Odds")
        view2 = PopulationView(pop, [1, 2], label="OneTwo")
        view_iv = view.initial_values
        self.assertEquals(3, len(view_iv))
        self.assertEquals([-65, -65], view_iv["v"])
        view.initialize(v=-60)
        self.assertEquals([-65, -60, -65, -60, -65], pop.get_initial_value("v"))
        self.assertEquals([-60, -60], view.initial_values["v"])
        self.assertEquals([-60, -65], view2.initial_values["v"])
        rand_distr = RandomDistribution("uniform",
                                        parameters_pos=[-65.0, -55.0],
                                        rng=NumpyRNG(seed=85524))
        view.initialize(v=rand_distr)
        self.assertEquals([-64.43349869042906, -63.663421790102184],
                         view.initial_values["v"])
        view.initialize(v=lambda i: -65 + i / 10.0)
        self.assertEquals([-64.9, -64.7], view.initial_values["v"])
        sim.end()

    def test_projection(self):
        sim.setup(timestep=1.0)
        pop = sim.Population(5, sim.IF_curr_exp(), label="pop_1")
        view = PopulationView(pop, [1, 3], label="Odds")
        try:
            sim.Projection(pop, view, sim.OneToOneConnector())
        except NotImplementedError:
            pass  # Exceptable but better if it worked
        with pytest.raises(ConfigurationException):
            sim.Projection(pop, "SOMETHING WIERD", sim.OneToOneConnector())
