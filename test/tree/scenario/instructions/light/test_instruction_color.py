import unittest
from tree.scenario.instructions.light.Instruction_color import Instruction_color, Color, RESOLUTION
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionColor(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.light, self.dimmer, self.color = Mock(), Mock(), 100, "0xFF00FF"
        self.light.dimmer = 0
        self.light.color = Color("0x000000")
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_color(self.calculator, self.light, self.dimmer, self.duration, self.delay, False, self.color)
        self.state = False
        self.count = 0
        def lock():
            self.assertFalse(self.state)
            self.state = True
            self.count += 1

        def unlock():
            self.assertTrue(self.state)
            self.state = False
            self.count += 1

        def connect():
            self.assertTrue(self.state)
            self.count += 1
            return True

        def disconnect():
            self.assertTrue(self.state)
            self.count += 1

        def test():
            self.assertTrue(self.state)
            return False
        self.light.lock.side_effect = lock
        self.light.test.side_effect = test
        self.light.unlock.side_effect = unlock
        self.light.connect.side_effect = connect
        self.light.disconnect.side_effect = disconnect


    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 3)
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.duration)
        self.assertEqual(self.calculator.eval.call_args_list[1][0][0], self.color)
        self.assertEqual(self.calculator.eval.call_args_list[2][0][0], self.dimmer)

    @parameterized.expand(((10,), (0,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_duration(self, duration, time, sleep):
        def set_color(dimmer, color):
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            if duration == 0:
                self.assertEqual(color, self.color)
                self.assertEqual(dimmer, self.dimmer)
                self.assertEqual(self.light.set_color.call_count, 1)
            else:
                self.assertEqual(Color(color), Color(self.color).dim(dimmer))
                nb_call = self.light.set_color.call_count
                self.assertEqual(sleep.call_count, nb_call-1)
                if sleep.call_count:
                    self.assertEqual(sleep.call_args[0][0], 1/RESOLUTION)
                if nb_call not in (30, 58, 59):
                    self.assertEqual(int(dimmer), int(self.dimmer*((self.light.set_color.call_count-1)/(duration*RESOLUTION))))
            self.count += 1

        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return duration
            return val

        self.light.set_color.side_effect = set_color
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.count, RESOLUTION*duration+5)
        self.assertEqual(self.light.set_color.call_count, RESOLUTION*duration+1)
        self.assertEqual(self.light.set_color.call_args[0][0], self.dimmer)
        self.assertEqual(self.light.set_color.call_args[0][1], self.color)
        self.assertFalse(self.state)

    @parameterized.expand(((20, 0xff00ff), (100, 0), (0, 0xff00ff), (0, 0)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_colors_dimmer(self, dimmer, color, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            elif val == self.color:
                return color
            elif val == self.dimmer:
                return dimmer
            return val
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertFalse(self.state)
        if not(dimmer != self.dimmer and color != int(self.color, 16)):
            self.assertEqual(self.light.set_color.call_count, RESOLUTION*10+1)
            self.assertEqual(self.light.set_color.call_args[0][0], dimmer)
            self.assertEqual(self.light.set_color.call_args[0][1], str(Color(color)))

    @patch("time.sleep")
    @patch("time.time")
    def test_run_no_connection(self, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            return val
        self.calculator.eval.side_effect = evaluate
        self.light.connect.side_effect = lambda: False
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.light.set_color.call_count, 0)
        self.assertEqual(self.count,2) 
        self.assertFalse(self.state)

    @parameterized.expand(((10,), (1,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_kill(self, kill, time, sleep):
        self.kill = 0
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            return val

        def test():
            self.kill += 1
            return self.kill == kill

        def set_color(color, dimmer):
            self.assertTrue(self.state)
            self.count += 1

        self.light.set_color.side_effect = set_color
        self.calculator.eval.side_effect = evaluate
        self.light.test.side_effect = test
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.light.set_color.call_count, kill-1-(kill!=1))
        self.assertEqual(self.count,kill+1+(kill==1)) 
        self.assertFalse(self.state)

    def test_str(self):
        self.assertTrue("color" in str(self.inst))
        self.assertTrue(str(self.color) in str(self.inst))
        self.assertTrue(str(self.dimmer) in str(self.inst))
 
