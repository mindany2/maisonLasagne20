import unittest
from tree.connected_objects.dmx.Dmx_device import Dmx_device
from unittest.mock import Mock
from mock import patch
import timeout_decorator

@patch('time.sleep', return_value=None)
class TestDmxDevice(unittest.TestCase):
    def test_init(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 59, dmx)
        self.assertEqual(device.dmx, dmx)
        self.assertEqual(device.relay, relay)

    def test_set(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 59, dmx)
        channel = Mock()
        channel.value = 3
        with self.assertRaises(AssertionError):
            device.set(channel, 42)
        device.connect()
        device.set(channel, 42)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0][0], 59+3-1, 42)

    def test_connect(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 59, dmx)
        device.connect()
        self.assertEqual(dmx.connect.call_count, 1)
        self.assertEqual(dmx.connect.call_args[0][0], 59)

    def test_took_time_to_connect(self, sleep):
        relay, dmx = Mock(), Mock()
        dmx.connect.return_value = False
        device = Dmx_device("test", relay, 59, dmx)
        @timeout_decorator.timeout(0.01)
        def connect(device):
            device.connect()
        with self.assertRaises(timeout_decorator.TimeoutError):
            connect(device)
        self.assertGreater(sleep.call_count, 1)

    def test_disconnect(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 59, dmx)
        device.connect()
        device.disconnect()
        self.assertEqual(dmx.disconnect.call_count, 1)
        self.assertEqual(dmx.disconnect.call_args[0][0], 59)

    def test_eq(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 59, dmx)
        self.assertEqual(device, device)
        self.assertNotEqual(device, 42)
        device2 = Dmx_device("test", Mock(), 59, dmx)
        self.assertNotEqual(device, device2)
        device2 = Dmx_device("test", relay, 58, dmx)
        self.assertNotEqual(device, device2)
        device2 = Dmx_device("test", relay, 59, Mock())
        self.assertNotEqual(device, device2)

    def test_str(self, sleep):
        relay, dmx = Mock(), Mock()
        device = Dmx_device("test", relay, 5519, dmx)
        self.assertTrue(str(id(dmx)) in str(device)) 
        self.assertTrue("5519" in str(device)) 




