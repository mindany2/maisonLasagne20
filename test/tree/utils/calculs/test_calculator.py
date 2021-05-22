import unittest
from tree.utils.calculs.Calculator import Calculator
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestCalculator(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.variable = Mock()
        self.calculator = Calculator()

    def test_add(self):
        self.calculator.add(self.variable)
        self.assertTrue(self.variable in self.calculator.get_list_variables())

    @parametrize("exp, result", [("1+2", 3), ("8*2", 16), ("var*2", 42*2), ("var/(1-5)", -42/4),
        ("randint(1,1)", 1), ("False*2", 0), ("True+1", 2), ("var==42", 1), ("var != 42", 0), ("var**2", 42**2), ("*6", None), ("va+1", None)])
    def test_eval(self, exp, result):
        def raise_error(e):
            raise Exception(e)
        self.expression = Mock()
        self.expression.__str__ = lambda x: exp
        self.expression.raise_error.side_effect = raise_error
        self.variable.get.return_value = 42
        self.variable.name = "var"
        self.calculator.add(self.variable)
        if result is None:
            with self.assertRaises(Exception):
                self.assertEqual(self.calculator.eval(self.expression), result)
        else:
            self.assertEqual(self.calculator.eval(self.expression), result)

    def test_reset(self):
        self.calculator.add(self.variable)
        self.variable1 = Mock()
        self.calculator.add(self.variable1)
        self.calculator.reset()
        for var in [self.variable, self.variable1]:
            self.assertEqual(var.reset.call_count, 1)

    def test_get(self):
        self.variable.name = "var"
        self.calculator.add(self.variable)
        self.variable1 = Mock()
        self.variable1.name = "var1"
        self.calculator.add(self.variable1)
        for var in [self.variable, self.variable1]:
            self.assertEqual(self.calculator.get(var.name), var)

    def test_str(self):
        self.variable.name = "var"
        self.calculator.add(self.variable)
        self.variable1 = Mock()
        self.variable1.name = "var1"
        self.calculator.add(self.variable1)
        for var in [self.variable, self.variable1]:
            self.assertTrue(str(var) in str(self.calculator))



 
