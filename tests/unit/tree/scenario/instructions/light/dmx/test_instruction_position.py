import unittest
from tree.scenario.instructions.light.dmx.Instruction_position import Instruction_position, RESOLUTION
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionPosition(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.light, self.pan, self.tilt = Mock(), Mock(), 100, 212
        self.light.get_position.return_value = 0,0
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_position(self.calculator, self.light, self.pan, self.tilt, self.duration, self.delay, False)
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
        self.light.lock_position.side_effect = lock
        self.light.test_position.side_effect = test
        self.light.unlock_position.side_effect = unlock
        self.light.connect.side_effect = connect
        self.light.disconnect.side_effect = disconnect


    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 3)
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.duration)
        self.assertEqual(self.calculator.eval.call_args_list[1][0][0], self.pan)
        self.assertEqual(self.calculator.eval.call_args_list[2][0][0], self.tilt)

    @parameterized.expand(((10,), (0,)))
    @patch("time.sleep")
    @patch("time.time", return_value=0)
    def test_run_duration(self, duration, time, sleep):
        def set_position(pan, tilt):
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            if duration == 0:
                self.assertEqual(tilt, self.tilt)
                self.assertEqual(pan, self.pan)
                self.assertEqual(self.light.set_position.call_count, 1)
            else:
                nb_call = self.light.set_position.call_count
                self.assertEqual(sleep.call_count, nb_call-1)
                if sleep.call_count:
                    self.assertEqual(sleep.call_args[0][0], 1/RESOLUTION)
                if nb_call not in (30, 58, 59):
                    self.assertEqual(int(pan), int(self.pan*((self.light.set_position.call_count-1)/(duration*RESOLUTION))))
            self.count += 1

        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return duration
            return val

        self.light.set_position.side_effect = set_position
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.count, RESOLUTION*duration+3)
        self.assertEqual(self.light.set_position.call_count, RESOLUTION*duration+1)
        self.assertEqual(self.light.set_position.call_args[0][0], self.pan)
        self.assertEqual(self.light.set_position.call_args[0][1], self.tilt)
        self.assertFalse(self.state)

    @parameterized.expand(((20, 52), (100, 0), (0, 255), (0, 0)))
    @patch("time.sleep")
    @patch("time.time", return_value=0)
    def test_run_position(self, pan, tilt, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            elif val == self.tilt:
                return tilt
            elif val == self.pan:
                return pan
            return val
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertFalse(self.state)
        if not(pan != self.pan and tilt != self.tilt):
            self.assertEqual(self.light.set_position.call_count, RESOLUTION*10+1)
            self.assertEqual(self.light.set_position.call_args[0][0], pan)
            self.assertEqual(self.light.set_position.call_args[0][1], tilt)

    @parameterized.expand(((10,), (1,)))
    @patch("time.sleep")
    @patch("time.time", return_value=0)
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

        def set_position(tilt, pan):
            self.assertTrue(self.state)
            self.count += 1

        self.light.set_position.side_effect = set_position
        self.calculator.eval.side_effect = evaluate
        self.light.test_position.side_effect = test
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.light.set_position.call_count, kill-1)
        self.assertEqual(self.count,kill+1) 
        self.assertFalse(self.state)

    def test_str(self):
        self.assertTrue("position" in str(self.inst))
        self.assertTrue(str(self.tilt) in str(self.inst))
        self.assertTrue(str(self.pan) in str(self.inst))
 
