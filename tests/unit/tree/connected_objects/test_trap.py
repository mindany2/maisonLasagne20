import unittest
from tree.connected_objects.Trap import Trap, STATE as TRAP_STATE
from In_out.external_boards.relay.Relay import STATE
from unittest.mock import Mock
from mock import patch
import time

@patch('time.sleep', return_value=None)
class TestLed(unittest.TestCase):
    def test_init(self, sleep):
        up, down, magnet, sensor = [Mock()]*4
        sensor.capture.return_value = True
        trap = Trap("test", up, down, magnet, sensor)
        self.assertEqual(trap.get_state(), TRAP_STATE.up)
        sensor.capture.return_value = False
        trap = Trap("test", up, down, magnet, sensor)
        self.assertEqual(trap.get_state(), TRAP_STATE.down)

    #TODO The rest

