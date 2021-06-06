import unittest
from tree.scenario.instructions.light.dmx.Instruction_color_wheel import Instruction_color_wheel, COLOR
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
        self.color, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_color_wheel(self.calculator, self.lyre, self.color, self.duration, self.delay, False)

        self.count = 0
        def color_wheel(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.count += 1
        self.lyre.set_color.side_effect = color_wheel

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.color)

    @parameterized.expand(((0,), (6,)))
    def test_run(self, color):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.color:
                return color
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.lyre.set_color.call_args[0][0], [x for x in COLOR][color])
        self.assertEqual(self.count, 1)


    def test_str(self):
        self.assertTrue("color_wheel" in str(self.inst))
        self.assertTrue(str(self.lyre.name) in str(self.inst))
        self.assertTrue(str(self.color) in str(self.inst))
 
