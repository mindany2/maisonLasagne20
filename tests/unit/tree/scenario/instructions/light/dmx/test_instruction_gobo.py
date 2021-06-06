import unittest
from tree.scenario.instructions.light.dmx.Instruction_gobo import Instruction_gobo, GOBO
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionColorWheel(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.lyre, self.delay = Mock(), Mock(), Mock()
        self.gobo, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_gobo(self.calculator, self.lyre, self.gobo, self.duration, self.delay, False)

        self.count = 0
        def gobo(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.count += 1
        self.lyre.set_gobo.side_effect = gobo

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.gobo)

    @parameterized.expand(((0,), (6,)))
    def test_run(self, gobo):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.gobo:
                return gobo
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.lyre.set_gobo.call_args[0][0], [x for x in GOBO][gobo])
        self.assertEqual(self.count, 1)


    def test_str(self):
        self.assertTrue("gobo" in str(self.inst))
        self.assertTrue(str(self.lyre.name) in str(self.inst))
        self.assertTrue(str(self.gobo) in str(self.inst))
 
