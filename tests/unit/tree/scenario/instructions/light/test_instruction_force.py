import unittest
from tree.scenario.instructions.light.Instruction_force import Instruction_force
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionForce(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.light, self.delay = Mock(), Mock(), Mock()
        self.arg, self.condition = Mock(), Mock()
        self.duration = 0
        self.inst = Instruction_force(self.calculator, self.light, self.arg, self.duration, self.delay, False)

        self.state = False
        self.count = 0
        def lock():
            self.assertFalse(self.state)
            self.state = True
            self.count += 1

        def force(state):
            self.assertEqual(self.delay.wait.call_count, 1)
            self.assertTrue(self.state)
            self.count += 1

        def unlock():
            self.assertTrue(self.state)
            self.state = False
            self.count += 1

        self.light.lock.side_effect = lock
        self.light.unlock.side_effect = unlock
        self.light.force_relay.side_effect = force

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.arg)

    @parameterized.expand(((True,), (False,)))
    def test_run(self, state):
        def evals(args, inst):
            self.assertEqual(self.inst, inst)
            if args == self.arg:
                return state
            return args
        self.calculator.eval.side_effect = evals
        self.inst.run()
        self.assertEqual(self.light.force_relay.call_args[0][0], state)
        self.assertEqual(self.count, 3)


    def test_str(self):
        self.assertTrue("force" in str(self.inst))
        self.assertTrue(str(self.light.name) in str(self.inst))
        self.assertTrue(str(self.arg) in str(self.inst))
 
