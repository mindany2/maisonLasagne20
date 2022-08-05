import unittest
from tree.scenario.instructions.Instruction_mode import Instruction_mode
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionMode(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.tree, self.delay = Mock(), Mock(), Mock()
        self.name_mode, self.condition = Mock(), Mock()
        self.inst = Instruction_mode(self.calculator, self.tree, self.name_mode, self.delay, self.condition, False)

    @parameterized.expand(((True,), (False,)))
    def test_run(self, evals):
        self.calculator.eval.return_value = evals
        self.inst.run()
        self.assertEqual(self.tree.change_mode.call_count, int(evals))
        if evals:
            self.assertEqual(self.tree.change_mode.call_args[0][0], self.name_mode)

    def test_str(self):
        self.assertTrue("mode" in str(self.inst))
        self.assertTrue(str(self.name_mode) in str(self.inst))
 
