import os
import shutil
import unittest
from pyNN.random import RandomDistribution
from spynnaker.pyNN.utilities import utility_calls
from spynnaker8 import setup


class TestUtilityCalls(unittest.TestCase):
    def test_check_directory_exists(self):
        utility_calls.check_directory_exists_and_create_if_not(os.path.dirname(
            os.path.realpath(__file__)))
        self.assertTrue(os.path.exists(os.path.dirname(
            os.path.realpath(__file__))))

    def test_check_directory_not_exists(self):
        test_dir = os.path.join(os.path.dirname(__file__),
                                "test_utility_call")
        test_file = os.path.join(test_dir, "test")
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print("Directory existed. Deleting...")

        utility_calls.check_directory_exists_and_create_if_not(test_file)

        if not os.path.exists(test_dir):
            raise AssertionError("Directory was not created")
        print("Directory created successfully. Deleting...")
        os.rmdir(test_dir)

    @unittest.skip("Not implemented")
    def test_is_conductance(self):
        self.assertEqual(True, False, "NotImplementedError")

    @unittest.skip("Not implemented")
    def test_check_weight(self):
        self.assertEqual(True, False, "NotImplementedError")

    @unittest.skip("Not implemented")
    def test_check_delay(self):
        self.assertEqual(True, False, "NotImplementedError")

    @unittest.skip("Not implemented")
    def test_get_region_base_address_offset(self):
        self.assertEqual(True, False, "Test not implemented yet")

    @unittest.skip("Not implemented")
    def test_get_ring_buffer_to_input_left_shift(self):
        self.assertEqual(True, False, "Test not implemented yet")

    def test_convert_param_to_numpy_random_distribution(self):
        setup(1.0)
        random = RandomDistribution("uniform", [0, 1])
        single_value = utility_calls.convert_param_to_numpy(random, 1)
        multi_value = utility_calls.convert_param_to_numpy(random, 10)

        self.assertTrue(hasattr(single_value, "__iter__"))
        self.assertEqual(len(single_value), 1)
        self.assertTrue(hasattr(multi_value, "__iter__"))
        self.assertEqual(len(multi_value), 10)

    @unittest.skip("Not implemented")
    def test_convert_param_to_numpy_iterable(self):
        self.assertEqual(True, False, "Test not implemented yet")

    @unittest.skip("Not implemented")
    def test_convert_param_to_numpy_random(self):
        self.assertEqual(True, False, "Test not implemented yet")

    @unittest.skip("Not implemented")
    def test_convert_param_to_numpy_exception(self):
        self.assertEqual(True, False, "Test not implemented yet")


if __name__ == '__main__':
    unittest.main()
