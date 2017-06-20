import unittest

from spynnaker.pyNN.models.neuron.builds.if_cond_exp_base import IFCondExpBase
import spynnaker8 as p


class TestParameters(unittest.TestCase):

    def test_class_default_parameters(self):
        self.assertEqual(IFCondExpBase.default_parameters,
                         p.IF_cond_exp.default_parameters)

    def test_module_default_parameters(self):
        module = p.IF_cond_exp()
        self.assertEqual(IFCondExpBase.default_parameters,
                         module.default_parameters)

    def test_class_get_parameter_names(self):
        self.assertEqual(IFCondExpBase.default_parameters.keys(),
                         p.IF_cond_exp.get_parameter_names())

    def test_module_get_parameter_names(self):
        module = p.IF_cond_exp()
        self.assertEqual(IFCondExpBase.default_parameters.keys(),
                         module.get_parameter_names())
