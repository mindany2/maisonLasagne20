import unittest
from tree.connected_objects.dmx.Strombo import Strombo, CHANNEL
from unittest.mock import Mock
from mock import patch
import timeout_decorator

@patch('time.sleep', return_value=None)
class TestStrombo(unittest.TestCase):

    def test_init(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)
        self.assertEqual(strombo.dimmer, 0)
        self.assertEqual(strombo.strombo, 0)

    def test_dimmer(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)

        strombo.connect()
        strombo.set_dimmer(12)
        self.assertEqual(strombo.dimmer, 12)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (52+CHANNEL.dimmer.value-1, 12))
        strombo.disconnect()

    def test_strombo(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)

        strombo.connect()
        strombo.set_strombo(45)
        self.assertEqual(strombo.strombo, 45)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (52+CHANNEL.strombo.value-1, 45))
        strombo.disconnect()

    def test_reload(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)
        strombo.connect()
        strombo.set_dimmer(48)
        strombo.set_strombo(14)
        strombo2 = Strombo("test", relay, 53, dmx)
        strombo2.reload(strombo)
        self.assertEqual(strombo.dimmer, 48)
        self.assertEqual(strombo.strombo, 14)

    def test_eq(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)
        strombo2 = Strombo("test", relay, 52, dmx)
        self.assertEqual(strombo, strombo)
        self.assertEqual(strombo2, strombo)
        self.assertNotEqual(strombo2, 4)
        strombo.connect()
        strombo.set_dimmer(48)
        self.assertNotEqual(strombo2, strombo)
        strombo.set_dimmer(0)
        self.assertEqual(strombo2, strombo)
        strombo.set_strombo(48)
        self.assertNotEqual(strombo2, strombo)
        strombo.set_strombo(0)
        self.assertEqual(strombo2, strombo)

    def test_str(self, sleep):
        relay, dmx = Mock(), Mock()
        strombo = Strombo("test", relay, 52, dmx)
        self.assertTrue("Strombo" in str(strombo))


 
