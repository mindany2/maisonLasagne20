import unittest
from tree.scenario.instructions.Instruction_PC import Instruction_PC, ACTIONS, Press_key, Press_mouse
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionPC(unittest.TestCase):
    def before(self, action):
        self.calculator, self.pc, self.action, self.args = Mock(), Mock(), action, ["arg1", "arg2", "double"]
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_PC(self.calculator, self.pc, self.action, self.args, self.duration, self.delay, False)

    
    @parameterized.expand(((ACTIONS.power_on,), (ACTIONS.power_off,), (ACTIONS.keys,), (ACTIONS.mouse,)))
    @patch.object(Press_mouse, "__init__", return_value=None)
    @patch.object(Press_key, "__init__", return_value=None)
    @patch("time.sleep")
    def test_run(self, action, sleep, press_key, press_mouse):
        self.before(action)
        self.state = False
        self.count = 0
        def lock():
            self.assertFalse(self.state)
            self.state = True
            self.assertTrue(self.delay.wait.call_count)
            self.count += 1

        def unlock():
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            self.state = False
            self.count += 1

        def power_off():
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            self.assertEqual(self.action, ACTIONS.power_off)
            self.count += 1

        def connect():
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            self.assertEqual(self.action, ACTIONS.power_on)
            self.count += 1

        def send(args):
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            self.count += 1
            if self.action == ACTIONS.keys:
                self.assertEqual(press_key.call_count, 1)
                self.assertEqual(press_mouse.call_count, 0)
                self.assertEqual(press_key.call_args[0][0], self.args)
                self.assertTrue(isinstance(args, Press_key))

            elif self.action == ACTIONS.mouse:
                self.assertEqual(press_key.call_count, 0)
                self.assertEqual(press_mouse.call_count, 1)
                self.assertEqual(press_mouse.call_args[0][0], self.args[0])
                self.assertEqual(press_mouse.call_args[0][1], self.args[1])
                self.assertFalse(press_mouse.call_args[0][2])
                self.assertTrue(press_mouse.call_args[0][3])
            else:
                raise Exception()

        self.pc.lock.side_effect = lock
        self.pc.unlock.side_effect = unlock
        self.pc.power_off.side_effect = power_off
        self.pc.connect.side_effect = connect
        self.pc.send.side_effect = send
        self.inst.run()
        self.assertEqual(self.count, 3)
        if self.action == ACTIONS.keys:
            self.assertEqual(sleep.call_count, 1)

    def test_str(self):
        self.before(ACTIONS.power_off)
        self.assertTrue("PC" in str(self.inst))
        self.assertTrue(str(self.action) in str(self.inst))
        self.assertTrue(str(self.args) in str(self.inst))
 
