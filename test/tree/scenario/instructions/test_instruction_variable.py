import unittest
from tree.scenario.instructions.Instruction_variable import Instruction_variable
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionVariable(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.variable, self.value = Mock(), Mock(), "42"
        self.duration, self.delay = Mock(), Mock()
        self.inst = Instruction_variable(self.calculator, self.variable, self.value, self.duration, self.delay, True)

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.value)

    def test_run(self):
        def var_set(value, duration):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.assertEqual(value, self.calculator.eval())
            self.assertEqual(duration, self.calculator.eval())
        self.variable.set.side_effect = var_set
        self.inst.run()
        self.assertEqual(self.variable.set.call_count, 1)
 
    def test_str(self):
        self.assertTrue("variable" in str(self.inst))
        self.assertTrue(str(self.variable.name) in str(self.inst))
        self.assertTrue(str(self.value) in str(self.inst))
