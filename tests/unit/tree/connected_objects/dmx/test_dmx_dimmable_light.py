import unittest
from tree.connected_objects.dmx.Dmx_dimmable_light import Dmx_dimmable_light
from In_out.external_boards.relay.Relay import STATE
from unittest.mock import Mock
from mock import patch

@patch('time.sleep', return_value=None)
class TestDmxDimmableLight(unittest.TestCase):
    def test_init(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        self.assertEqual(light.dimmer, 0)

    def test_connect(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)

    def test_connect_already_on(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.dimmer = 50
        light.connect()
        self.assertEqual(relay.set.call_count, 0)

    def test_disconnect(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.disconnect()
        self.assertEqual(relay.set.call_count, 2)
        self.assertEqual(relay.set.call_args[0][0], STATE.OFF)

    def test_disconnect_on(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.set_dimmer(50)
        light.disconnect()
        self.assertEqual(relay.set.call_count, 1)
        self.assertEqual(relay.set.call_args[0][0], STATE.ON)

    def test_set_dimmer(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.set_dimmer(50)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42, 50))

    def test_reload(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.set_dimmer(50)
        light.disconnect()
        light2 = Dmx_dimmable_light("test2", relay, 43, dmx)
        light2.reload(light)
        self.assertEqual(light2.dimmer, light.dimmer)

    def test_eq(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.set_dimmer(50)
        light.disconnect()
        light2 = Dmx_dimmable_light("test", relay, 42, dmx)
        self.assertEqual(light, light)
        self.assertNotEqual(light, light2)
        self.assertNotEqual(light, 42)

    def test_str(self, sleep):
        relay, dmx = Mock(), Mock()
        light = Dmx_dimmable_light("test", relay, 42, dmx)
        light.connect()
        light.set_dimmer(50)
        light.disconnect()
        self.assertTrue("50" in str(light))


