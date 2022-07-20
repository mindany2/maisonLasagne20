import unittest
from tree.scenario.instructions.Instruction_speaker import Instruction_speaker, RESOLUTION
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionSpeaker(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.speaker, self.volume = Mock(), Mock(), 100
        self.speaker.volume.return_value = 0
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_speaker(self.calculator, self.speaker, self.volume, self.duration, self.delay, False)
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
        self.speaker.lock.side_effect = lock
        self.speaker.test.side_effect = test
        self.speaker.unlock.side_effect = unlock
        self.speaker.connect.side_effect = connect
        self.speaker.disconnect.side_effect = disconnect

    def test_initialize(self):
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.duration)
        self.assertEqual(self.calculator.eval.call_args_list[1][0][0], self.volume)

    @parameterized.expand(((10,), (0,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_duration(self, duration, time, sleep):
        def change_volume(volume):
            self.assertTrue(self.state)
            self.assertTrue(self.delay.wait.call_count)
            if duration == 0:
                self.assertEqual(volume, self.volume)
                self.assertEqual(self.speaker.change_volume.call_count, 1)
            else:
                nb_call = self.speaker.change_volume.call_count
                self.assertEqual(sleep.call_count, nb_call-1)
                if sleep.call_count:
                    self.assertEqual(sleep.call_args[0][0], 1/RESOLUTION)
                if nb_call not in (30, 58, 59):
                    self.assertEqual(int(volume), int(self.volume*((self.speaker.change_volume.call_count-1)/(duration*RESOLUTION))))
            self.count += 1

        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return duration
            return val

        time.return_value = 42
        self.speaker.change_volume.side_effect = change_volume
        self.calculator.eval.side_effect = evaluate
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.count, RESOLUTION*duration+5)
        self.assertEqual(self.speaker.change_volume.call_count, RESOLUTION*duration+1)
        self.assertEqual(self.speaker.change_volume.call_args[0][0], self.volume)
        self.assertFalse(self.state)

    @parameterized.expand(((20,), (100,), (0,)))
    @patch("time.sleep")
    @patch("time.time")
    def test_run_volume(self, volume, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            elif val == self.volume:
                return volume
            return val
        self.calculator.eval.side_effect = evaluate
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertFalse(self.state)
        if volume:
            self.assertEqual(self.speaker.change_volume.call_count, RESOLUTION*10+1)
            self.assertEqual(self.speaker.change_volume.call_args[0][0], volume)

    @patch("time.sleep")
    @patch("time.time")
    def test_run_no_connection(self, time, sleep):
        def evaluate(val, inst):
            self.assertEqual(inst, self.inst)
            if val == self.duration:
                return 10
            return val
        self.calculator.eval.side_effect = evaluate
        self.speaker.connect.side_effect = lambda: False
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.speaker.change_volume.call_count, 0)
        self.assertEqual(self.speaker.connect.call_count, 1)
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

        def change_volume(volume):
            self.assertTrue(self.state)
            self.count += 1

        self.speaker.change_volume.side_effect = change_volume
        self.calculator.eval.side_effect = evaluate
        self.speaker.test.side_effect = test
        time.return_value = 42
        self.barrier = Mock()
        self.inst.run(self.barrier)
        self.assertEqual(self.speaker.change_volume.call_count, kill-1-(kill!=1))
        self.assertEqual(self.count,kill+1+(kill==1)) 
        self.assertFalse(self.state)

    def test_str(self):
        self.assertTrue("Speakers" in str(self.inst))
        self.assertTrue(str(self.speaker.name) in str(self.inst))
        self.assertTrue(str(self.volume) in str(self.inst))
 
