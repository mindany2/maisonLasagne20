import unittest
from tree.connected_objects.Lamp import Lamp
from tree.utils.Locker import Locker
from In_out.external_boards.relay.Relay import STATE
from unittest.mock import Mock

class TestLamp(unittest.TestCase):
    def test_connection(self):
        relay = Mock()
        lamp = Lamp("test", relay)
        lamp.connect()
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)
        lamp.disconnect()
        self.assertEqual(relay.set.call_count, 2)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)

    def test_force(self):
        relay = Mock()
        lamp = Lamp("test", relay)
        lamp.force_relay(True)
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)
        lamp.connect()
        self.assertEqual(relay.set.call_count, 1)
        lamp.disconnect()
        lamp.set_state(True)
        self.assertEqual(relay.set.call_count, 1)
        lamp.force_relay(False)
        self.assertEqual(relay.set.call_count, 2)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)
        lamp.connect()
        self.assertEqual(relay.set.call_count, 3)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)
        lamp.disconnect()
        self.assertEqual(relay.set.call_count, 4)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)

    def test_invert(self):
        relay = Mock()
        lamp = Lamp("test", relay, invert=True)
        lamp.set_state(False)
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)
        lamp.set_state(True)
        self.assertEqual(relay.set.call_count, 2)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)

    def test_reload(self):
        relay = Mock()
        lamp = Lamp("test", relay, invert=True)
        lamp.set_state(False)
        lamp.force_relay(True)
        relay2 = Mock()
        lamp2 = Lamp("test 2", relay2)
        lamp2.reload(lamp)
        self.assertEqual(lamp.state, STATE.ON)
        self.assertEqual(lamp.force, True)
        self.assertEqual(lamp.invert, True)

    def test_eq(self):
        relay = Mock()
        lamp = Lamp("test", relay, invert=True)
        lamp2 = Lamp("test", relay, invert=True)
        self.assertEqual(lamp, lamp2)
        lamp2 = Lamp("test ", relay, invert=True)
        self.assertNotEqual(lamp, lamp2)
        lamp2 = Lamp("test", Mock(), invert=True)
        self.assertNotEqual(lamp, lamp2)
        lamp2 = Lamp("test", relay)
        self.assertNotEqual(lamp, lamp2)
        lamp = Lamp("test", relay)
        lamp2 = Lamp("test", relay)
        lamp2.connect()
        self.assertNotEqual(lamp, lamp2)
        lamp2 = Lamp("test", relay)
        lamp2.force_relay(True)
        self.assertNotEqual(lamp, lamp2)
        self.assertNotEqual(lamp, 12)

    def test_str(self):
        relay = Mock()
        lamp = Lamp("test", relay, invert=True)
        self.assertTrue(str(id(relay)) in str(lamp))









