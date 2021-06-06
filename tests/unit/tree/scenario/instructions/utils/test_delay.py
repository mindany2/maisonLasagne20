import unittest
from tree.scenario.instructions.utils.Delay import Delay
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestDelay(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.manager, self.calculator, self.val = Mock(), Mock(), Mock()
        self.wait_for_beat = Mock()
        self.delay = Delay(self.manager, self.calculator, self.val, wait_for_beat=self.wait_for_beat)

    def test_initialize(self):
        self.delay.initialize()
        self.assertEqual(self.calculator.eval.call_count, 1)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.val)
    
    def test_get_wait_precedent(self):
        self.assertFalse(self.delay.get_wait_precedent())
        self.delay.wait_precedent = True
        self.assertTrue(self.delay.get_wait_precedent())

    @parameterized.expand(((125, 0), (0, 12), (20,5)))
    @patch("time.sleep")
    def test_wait(self, val, time_spent, sleep):
        def evals(arg):
            if arg == self.wait_for_beat:
                return 0
            elif arg == self.val:
                return val
        self.calculator.eval.side_effect = evals
        self.delay.wait(time_spent)
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.wait_for_beat)
        self.assertEqual(self.calculator.eval.call_args_list[1][0][0], self.val)
        if val > time_spent:
            self.assertEqual(sleep.call_count, 1)
            self.assertEqual(sleep.call_args[0][0], val-time_spent)
        else:
            self.assertEqual(sleep.call_count, 0)

    @parameterized.expand(((0,), (12, )))
    @patch("time.sleep")
    def test_wait_for_beat(self, nb_beat, sleep):
        def evals(arg):
            if arg == self.wait_for_beat:
                return nb_beat
            elif arg == self.val:
                return 52
        self.calculator.eval.side_effect = evals
        spotify = Mock()
        self.manager.get_spotify.return_value = spotify
        self.delay.wait()
        self.assertEqual(self.calculator.eval.call_count, 2+(nb_beat!=0))
        self.assertEqual(self.calculator.eval.call_args_list[0][0][0], self.wait_for_beat)
        self.assertEqual(self.calculator.eval.call_args_list[1+(nb_beat!=0)][0][0], self.val)
        if nb_beat:
            self.assertEqual(spotify.wait_for_beat.call_count, 1)
            self.assertEqual(spotify.wait_for_beat.call_args[0][0], nb_beat)
        else:
            self.assertEqual(spotify.wait_for_beat.call_count, 0)
        self.assertEqual(sleep.call_count, 1)
        self.assertEqual(sleep.call_args[0][0], 52)



    def test_str(self):
        self.assertTrue(str(self.val) in str(self.delay))
