import unittest
from tree.scenario.instructions.light.Instruction_dimmer import Instruction_dimmer, RESOLUTION
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionDimmer(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.light, self.dimmer = Mock(), Mock(), 100
        self.light.dimmer = 0
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_dimmer(self.calculator, self.light, self.dimmer, self.duration, self.delay, False)
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
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.duration)
        self.assertEqual(self.calculator.eval.call_args_list[1][0][0], self.dimmer)

    @parameterized.expand(((10,), (0,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_duration(self, duration, time, sleep):
        def set_dimmer(dimmer):
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            if duration == 0:
                self.assertEqual(dimmer, self.dimmer)
                self.assertEqual(self.light.set_dimmer.call_count, 1)
            else:
                nb_call = self.light.set_dimmer.call_count
                self.assertEqual(sleep.call_count, nb_call-1)
                if sleep.call_count:
                    self.assertEqual(sleep.call_args[0][0], 1/RESOLUTION)
                if nb_call not in (30, 58, 59):
                    self.assertEqual(int(dimmer), int(self.dimmer*((self.light.set_dimmer.call_count-1)/(duration*RESOLUTION))))
            self.count += 1

        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return duration
            return val

        time.return_value = 42
        self.light.set_dimmer.side_effect = set_dimmer
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.count, RESOLUTION*duration+5)
        self.assertEqual(self.light.set_dimmer.call_count, RESOLUTION*duration+1)
        self.assertEqual(self.light.set_dimmer.call_args[0][0], self.dimmer)
        self.assertFalse(self.state)

    @parameterized.expand(((20,), (100,), (0,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_dimmer(self, dimmer, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            elif val == self.dimmer:
                return dimmer
            return val
        self.calculator.eval.side_effect = evaluate
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertFalse(self.state)
        if dimmer:
            self.assertEqual(self.light.set_dimmer.call_count, RESOLUTION*10+1)
            self.assertEqual(self.light.set_dimmer.call_args[0][0], dimmer)

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
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.light.set_dimmer.call_count, 0)
        self.assertEqual(self.light.connect.call_count, 1)
        self.assertEqual(self.count, 2) 
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

        def set_dimmer(dimmer):
            self.assertTrue(self.state)
            self.count += 1

        self.light.set_dimmer.side_effect = set_dimmer
        self.calculator.eval.side_effect = evaluate
        self.light.test.side_effect = test
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.light.set_dimmer.call_count, kill-1-(kill!=1))
        self.assertEqual(self.count,kill+1+(kill==1)) 
        self.assertFalse(self.state)

    def test_str(self):
        self.assertTrue("dimmer" in str(self.inst))
        self.assertTrue(str(self.dimmer) in str(self.inst))
 
