import unittest
from tree.Mode import Mode
from unittest.mock import Mock, MagicMock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize
from In_out.dmx.controllers.KingDMX import KingDMX
from In_out.dmx.Wireless_transmitter import Wireless_transmitter
from In_out.utils.DMX import DMX
from In_out.external_boards.relay.Relay import STATE

class TestWireless(unittest.TestCase):

    @patch.object(DMX, "set_channel", return_value=None)
    @patch.object(DMX, "__init__", return_value=None)
    @patch.object(DMX, "clear_channels", return_value=None)
    def test_transmiters_connections_and_management(self, clear, init, set_channel):
        self.addr = "lol"
        self.relay1, self.relay2 = Mock(), Mock()
        self.transmitter1 = Wireless_transmitter(self.relay1, 0, 50)
        self.transmitter2 = Wireless_transmitter(self.relay2, 51, 60)
        self.controller = KingDMX(self.addr, transmitter=[self.transmitter1, self.transmitter2])
        self.assertEqual(init.call_count, 1)
        self.assertEqual(init.call_args[0][0], self.addr)

        self.assertTrue(self.controller.connect(10))
        self.assertEqual(self.relay1.set.call_count, 1)
        self.assertEqual(self.relay1.set.call_args[0][0], STATE.ON)

        self.assertFalse(self.controller.connect(55))
        self.assertEqual(self.relay2.set.call_count, 0)

        self.controller.set(10, 255)
        self.assertEqual(set_channel.call_count, 1)
        self.assertEqual(set_channel.call_args[0][0], 10)
        self.assertEqual(set_channel.call_args[0][1], 255)

        self.controller.set(50, 48)
        self.assertEqual(set_channel.call_count, 2)
        self.assertEqual(set_channel.call_args[0][0], 50)
        self.assertEqual(set_channel.call_args[0][1], 48)

        self.relay1.state = STATE.ON
        self.controller.disconnect(10)
        self.assertEqual(self.relay1.set.call_count, 2)
        self.assertEqual(self.relay1.set.call_args[0][0], STATE.OFF)

        self.assertTrue(self.controller.connect(55))
        self.assertEqual(self.relay2.set.call_count, 1)
        self.assertEqual(self.relay2.set.call_args[0][0], STATE.ON)

        self.controller.set(80, 12)
        self.assertEqual(set_channel.call_count, 3)
        self.assertEqual(set_channel.call_args[0][0], 80)
        self.assertEqual(set_channel.call_args[0][1], 12)



