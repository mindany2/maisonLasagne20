import unittest
from tree.connected_objects.dmx.Dmx_strip_led import Dmx_strip_led, CHANNEL
from In_out.external_boards.relay.Relay import STATE
from tree.utils.Color import Color
from unittest.mock import Mock
from mock import patch
import timeout_decorator

@patch('time.sleep', return_value=None)
class TestDmxStripLed(unittest.TestCase):
    def test_init(self, sleep):
        relay, dmx = Mock(), Mock()
        led = Dmx_strip_led("test", relay, 42, dmx)
        self.assertEqual(led.color, Color(0))
        self.assertEqual(led.dimmer, 0)

    def test_connect(self, sleep):
        relay, dmx = Mock(), Mock()
        led = Dmx_strip_led("test", relay, 42, dmx)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)
        led.set_color(100, "0x202020")
        led.disconnect()
        self.assertEqual(relay.set.call_count, 1)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count, 1)
        led.set_color(0, "0x000000")
        led.disconnect()
        self.assertEqual(relay.set.call_count, 2)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)

    def test_set(self, sleep):
        relay, dmx = Mock(), Mock()
        led = Dmx_strip_led("test", relay, 42, dmx)
        led.connect()
        led.set_color(50, "0x202020")
        self.assertEqual(dmx.set.call_count, len(CHANNEL))
        for call, channel in zip(dmx.set.call_args_list, CHANNEL):
            self.assertEqual(call[0], (42+channel.value-1, 0x10))
        self.assertEqual(led.dimmer, 50)
        self.assertEqual(led.color, Color("0x202020"))

    def test_str(self, sleep):
        relay, dmx = Mock(), Mock()
        led = Dmx_strip_led("test", relay, 42, dmx)
        led.connect()
        led.set_color(50, "0x202020")
        self.assertTrue("50" in str(led))
        self.assertTrue("0x202020" in str(led))

