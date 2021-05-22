import unittest
from tree.scenario.instructions.light.dmx.Instruction_strombo import Instruction_strombo
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionStrombo(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.lyre, self.delay = Mock(), Mock(), Mock()
        self.strombo, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_strombo(self.calculator, self.lyre, self.strombo, self.duration, self.delay, False)

        self.count = 0
        def strombo(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.count += 1
        self.lyre.set_strombo.side_effect = strombo

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.strombo)

    @parameterized.expand(((0,), (6,)))
    def test_run(self, strombo):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.strombo:
                return strombo
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.lyre.set_strombo.call_args[0][0], strombo)
        self.assertEqual(self.count, 1)


    def test_str(self):
        self.assertTrue("strombo" in str(self.inst))
        self.assertTrue(str(self.lyre.name) in str(self.inst))
        self.assertTrue(str(self.strombo) in str(self.inst))
 
