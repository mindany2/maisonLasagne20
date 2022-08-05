import unittest
from tree.scenario.instructions.light.dmx.Instruction_program import Instruction_program
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionProgram(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.lyre, self.delay = Mock(), Mock(), Mock()
        self.program, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_program(self.calculator, self.lyre, self.program, self.duration, self.delay, False)

        self.count = 0
        def program(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.count += 1
        self.lyre.set_program.side_effect = program

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.program)

    @parameterized.expand(((0,), (6,)))
    def test_run(self, program):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.program:
                return program
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.lyre.set_program.call_args[0][0], program)
        self.assertEqual(self.count, 1)


    def test_str(self):
        self.assertTrue("program" in str(self.inst))
        self.assertTrue(str(self.lyre.name) in str(self.inst))
        self.assertTrue(str(self.program) in str(self.inst))
 
