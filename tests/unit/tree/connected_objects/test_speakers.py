import unittest
from tree.connected_objects.Speakers import Speakers
from unittest.mock import Mock
from mock import patch

class TestSpeakers(unittest.TestCase):
    def test_get_volume(self):
        amp, zone = Mock(), Mock()
        zone.volume = 42
        speakers = Speakers("test", amp, zone)
        self.assertEqual(speakers.volume(), 42)

    def test_get_state(self):
        amp, zone = Mock(), Mock()
        amp.state.return_value = "kjhj"
        speakers = Speakers("test", amp, zone)
        self.assertEqual(speakers.state(), "kjhj")

    def test_connect(self):
        amp, zone = Mock(), Mock()
        amp.state.return_value = "kjhj"
        zone.volume = 0
        speakers = Speakers("test", amp, zone)
        self.assertEqual(speakers.connect(), "kjhj")
        self.assertEqual(amp.power_on.call_count, 1)

    def test_already_connect(self):
        amp, zone = Mock(), Mock()
        amp.state.return_value = "kjhj"
        zone.volume = 42
        speakers = Speakers("test", amp, zone)
        self.assertEqual(speakers.connect(), "kjhj")
        self.assertEqual(amp.power_on.call_count, 0)

    def test_disconnect(self):
        amp, zone = Mock(), Mock()
        zone.volume = 0
        speakers = Speakers("test", amp, zone)
        speakers.disconnect()
        self.assertEqual(amp.power_off.call_count, 1)

    def test_already_disconnect(self):
        amp, zone = Mock(), Mock()
        zone.volume = 52
        speakers = Speakers("test", amp, zone)
        speakers.disconnect()
        self.assertEqual(amp.power_off.call_count, 0)

    def test_change_volume(self):
        amp, zone = Mock(), Mock()
        zone.volume = 0
        zone.power = 0
        speakers = Speakers("test", amp, zone)
        speakers.connect()
        speakers.change_volume(42)
        self.assertEqual(amp.power_on.call_count, 1)
        self.assertEqual(zone.set_power.call_count, 1)
        self.assertEqual(zone.set_power.call_args[0][0], 1)
        self.assertEqual(zone.set_volume.call_count, 1)
        self.assertEqual(zone.set_volume.call_args[0][0], 42)

        speakers.change_volume(0)
        self.assertEqual(zone.set_power.call_count, 2)
        self.assertEqual(zone.set_power.call_args[0][0], 0)
        self.assertEqual(zone.set_volume.call_count, 2)
        self.assertEqual(zone.set_volume.call_args[0][0], 0)

    def test_eq(self):
        amp, zone = Mock(), Mock()
        speakers = Speakers("test", amp, zone)
        self.assertEqual(speakers, speakers)
        self.assertNotEqual(speakers, None)
        speakers2 = Speakers("test ", amp, zone)
        self.assertNotEqual(speakers, speakers2)
        speakers2 = Speakers("test", Mock(), zone)
        self.assertNotEqual(speakers, speakers2)
        speakers2 = Speakers("test", amp, Mock())
        self.assertNotEqual(speakers, speakers2)

    def test_str(self):
        amp, zone = Mock(), Mock()
        speakers = Speakers("test", amp, zone)
        self.assertTrue("test" in str(speakers))
        self.assertTrue(str(id(amp)) in str(speakers))
        self.assertTrue(str(id(zone)) in str(speakers))





