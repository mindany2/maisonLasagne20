import unittest
from tree.scenario.instructions.light.dmx.Instruction_speed import Instruction_speed
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionSpeed(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.lyre, self.delay = Mock(), Mock(), Mock()
        self.speed, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_speed(self.calculator, self.lyre, self.speed, self.duration, self.delay, False)

        self.count = 0
        def speed(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.count += 1
        self.lyre.set_speed.side_effect = speed

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.speed)

    @parameterized.expand(((0,), (6,)))
    def test_run(self, speed):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.speed:
                return speed
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.lyre.set_speed.call_args[0][0], speed)
        self.assertEqual(self.count, 1)


    def test_str(self):
        self.assertTrue("speed" in str(self.inst))
        self.assertTrue(str(self.lyre.name) in str(self.inst))
        self.assertTrue(str(self.speed) in str(self.inst))
 
