import unittest
from tree.scenario.instructions.Instruction import Instruction
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep

class TestInstruction(unittest.TestCase):

    @patch("uuid.uuid1", return_value=42)
    def test_init(self, uuid):
        calculator, delay = Mock(), Mock()
        inst = Instruction(calculator, 5, delay, False)
        self.assertEqual(inst.get_id(), 42)
        self.assertFalse(inst.current)

    def test_run(self):
        calculator, delay = Mock(), Mock()
        calculator.eval.return_value = 42
        inst = Instruction(calculator, "some value", delay, False)
        self.assertFalse(inst.current)
        inst.run(85)
        self.assertTrue(inst.current)
        self.assertEqual(calculator.eval.call_count, 1)
        self.assertEqual(calculator.eval.call_args[0], ("some value",inst))
        self.assertEqual(delay.wait.call_count, 1)
        self.assertEqual(delay.wait.call_args[0][0], 85)
        self.assertEqual(inst.duration, 42)
        inst.finish()
        self.assertFalse(inst.current)

    def test_reload(self):
        calculator, delay = Mock(), Mock()
        calculator.eval.return_value = 42
        inst = Instruction(calculator, "some value", delay, False)
        inst.reload(45)
        self.assertEqual(calculator.eval.call_count, 0)
        self.assertEqual(delay.wait.call_count, 0)
        self.assertEqual(inst.duration, 45)

        # test if the inst did not change the duration
        inst.run(0)
        self.assertEqual(calculator.eval.call_count, 1)
        self.assertEqual(calculator.eval.call_args[0], ("some value",inst))
        self.assertEqual(delay.wait.call_count, 1)
        self.assertEqual(delay.wait.call_args[0][0], 0)
        self.assertEqual(inst.duration, 42)

    def test_wait_precendent(self):
        calculator, delay = Mock(), Mock()
        delay.get_wait_precedent.return_value = 45
        inst = Instruction(calculator, 5, delay, False)
        self.assertEqual(inst.wait_precedent(), 45)
        self.assertEqual(delay.get_wait_precedent.call_count, 1)
        
    def test_wait_precendent_none(self):
        calculator = Mock()
        inst = Instruction(calculator, 5, None, False)
        self.assertFalse(inst.wait_precedent())

    def test_initialize(self):
        calculator, delay = Mock(), Mock()
        inst = Instruction(calculator, 5, delay, False)
        inst.initialize()
        self.assertEqual(delay.initialize.call_count, 1)
        self.assertEqual(calculator.eval.call_count, 1)
        self.assertEqual(calculator.eval.call_args[0][0], 5)

    def test_eq(self):
        calculator, delay = Mock(), Mock()
        inst = Instruction(calculator, 5, delay, False)
        inst2 = Instruction(calculator, 5, delay, False)
        self.assertEqual(inst, inst)
        self.assertNotEqual(inst, 12)
        inst2 = Instruction(Mock(), 5, delay, False)
        self.assertNotEqual(inst2, inst)
        inst2 = Instruction(calculator, 3, delay, False)
        self.assertNotEqual(inst2, inst)
        inst2 = Instruction(calculator, 5, Mock(), False)
        self.assertNotEqual(inst2, inst)
        inst2 = Instruction(calculator, 5, delay, True)
        self.assertNotEqual(inst2, inst)

    def test_str(self):
        calculator, delay = Mock(), Mock()
        inst = Instruction(calculator, "durtion", delay, False)
        self.assertTrue("durtion" in str(inst))
        self.assertTrue(str(delay) in str(inst))


