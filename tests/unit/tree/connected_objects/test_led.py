import unittest
from tree.connected_objects.Led import Led
from tree.utils.Locker import Locker
from tree.utils.Color import Color
from In_out.external_boards.relay.Relay import STATE
from unittest.mock import Mock
from mock import patch
import time

@patch('time.sleep', return_value=None)
class TestLed(unittest.TestCase):
    def test_init(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        self.assertEqual(led.color, Color(0))
        self.assertEqual(led.dimmer, 0)

    def test_right_connect(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count,1)
        self.assertEqual(sleep.call_count,1)
        self.assertEqual(relay.set.call_args[0][0],STATE.ON)
        self.assertEqual(controler.connect.call_count,1)
        self.assertEqual(controler.send_dimmer.call_count,1)
        self.assertEqual(controler.send_dimmer.call_args[0][0],100)

    def test_wrong_connect(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        controler.connect.return_value = False
        self.assertFalse(led.connect())
        self.assertEqual(relay.set.call_count,2)
        self.assertEqual(relay.set.call_args[0][0],STATE.OFF)
        self.assertEqual(controler.connect.call_count,1)

    def test_on_connect(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler, color = "0x202020")
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count,0)
        self.assertEqual(controler.connect.call_count,1)
        self.assertEqual(controler.send_dimmer.call_count,1)
        self.assertEqual(controler.send_dimmer.call_args[0][0],100)

    def test_force_connect(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        led.force_relay(True)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count,1)
        self.assertEqual(controler.connect.call_count,1)
        self.assertEqual(controler.send_dimmer.call_count,1)
        self.assertEqual(controler.send_dimmer.call_args[0][0],100)

    def test_not_connected(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler, color = "0x202020")
        led.disconnect()
        self.assertEqual(relay.set.call_count,0)
        self.assertEqual(controler.connect.call_count,0)
        self.assertEqual(controler.send_dimmer.call_count,0)

    def test_disconnect(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count,1)
        led.disconnect()
        self.assertEqual(sleep.call_count,2)
        self.assertEqual(relay.set.call_count,2)
        self.assertEqual(relay.set.call_args[0][0],STATE.OFF)
        self.assertEqual(controler.disconnect.call_count,1)

    def test_disconnect_not(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        self.assertTrue(led.connect())
        self.assertEqual(relay.set.call_count,1)
        led.set_color(200, 0x505050)
        led.disconnect()
        self.assertEqual(sleep.call_count,2)
        self.assertEqual(relay.set.call_count,1)
        self.assertEqual(relay.set.call_args[0][0],STATE.ON)
        self.assertEqual(controler.disconnect.call_count,1)

    def test_set_color(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        with self.assertRaises(AssertionError):
            led.set_color(50, 0x545454)
        led.connect()
        led.set_color(50, 0x545454)
        self.assertEqual(controler.send_color.call_count,1)
        self.assertEqual(controler.send_color.call_args[0][0], Color("2a2a2a"))
        led.set_color(100, 0x545454)
        self.assertEqual(controler.send_color.call_count,2)
        self.assertEqual(controler.send_color.call_args[0][0], Color("545454"))
        
    def test_repair(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        led.repair()
        # TODO 
 
    def test_reload(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        led.connect()
        led.set_color(12, 0x424242)
        relay2, controler2 = Mock(), Mock()
        led2 = Led("test", relay2, controler2)
        led2.reload(led)
        self.assertEqual(led2.dimmer, 12)
        self.assertEqual(led2.color, Color("424242"))

    def test_eq(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        led2 = Led("test ", relay, controler)
        self.assertEqual(led, led)
        self.assertNotEqual(led, None)
        self.assertNotEqual(led, led2)
        led2 = Led("test", Mock(), controler)
        self.assertNotEqual(led, led2)
        led2 = Led("test", relay, Mock())
        self.assertNotEqual(led, led2)
        led2 = Led("test", relay, controler)
        self.assertEqual(led, led2)
        led2.connect()
        led2.set_color(0, 0x121212)
        self.assertNotEqual(led, led2)
        led2.set_color(100, 0x000000)
        self.assertNotEqual(led, led2)
        led2.set_color(0, 0)
        self.assertNotEqual(led, led2)
        led2.disconnect()
        self.assertEqual(led, led2)

    def test_str(self, sleep):
        relay, controler = Mock(), Mock()
        led = Led("test", relay, controler)
        self.assertEqual(str(led).count("test"), 1)
        self.assertEqual(str(led).count(str(id(relay))), 1)
        self.assertEqual(str(led).count(str(id(controler))), 1)
        led.connect()
        led.set_color(42, 0xff00ff)
        self.assertTrue(str(led).count("42"))
        self.assertTrue(str(led).count("0xFF00FF"))

if __name__ == "__main__":
    unittest.main()
