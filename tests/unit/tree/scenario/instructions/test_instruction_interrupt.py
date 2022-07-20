import unittest
from tree.scenario.instructions.Instruction_interrupt import Instruction_interrupt
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest

class TestInstructionInterrupt(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.connection, self.delay = Mock(), Mock(), Mock()
        self.state = 48
        self.inst = Instruction_interrupt(self.calculator, self.connection, "test", self.state, self.delay, False)

    def test_run(self):
        self.lock = False
        def connect():
            self.lock = True
        def disconnect():
            self.lock = False
        def test(name, state):
            self.assertTrue(self.lock)
            self.assertEqual(name, "test")
            self.assertEqual(self.calculator.eval.call_count, 2)
            self.assertEqual(self.calculator.eval.call_args[0][0], self.state)
            self.assertEqual(state, self.calculator.eval())
        self.connection.lock.side_effect = connect
        self.connection.test.return_value = False
        self.connection.unlock.side_effect = disconnect
        self.connection.send_interrupt.side_effect = test
        self.inst.run()

    def test_run_fail(self):
        self.connection.test.return_value = True
        self.assertEqual(self.connection.send_interrupt.call_count, 0)

    def test_str(self):
        self.assertTrue("inter" in str(self.inst))
        self.assertTrue(str(self.connection.name) in str(self.inst))
        self.assertTrue("test" in str(self.inst))



