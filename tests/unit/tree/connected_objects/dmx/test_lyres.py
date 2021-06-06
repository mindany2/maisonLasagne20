import unittest
from tree.connected_objects.dmx.Lyre import Lyre, COLOR, GOBO, CHANNEL
from unittest.mock import Mock
from mock import patch
import timeout_decorator

@patch('time.sleep', return_value=None)
class TestLyre(unittest.TestCase):
    def test_init(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        self.assertEqual(lyre.pan, 0) 
        self.assertEqual(lyre.tilt, 0) 
        self.assertEqual(lyre.speed_motor, 0) 
        self.assertEqual(lyre.speed, 0) 
        self.assertEqual(lyre.strombo, 0) 
        self.assertEqual(lyre.dimmer, 0) 
        self.assertEqual(lyre.gobo, GOBO.simple_round) 
        self.assertEqual(lyre.color, COLOR.white) 

    def test_position(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        with self.assertRaises(AssertionError):
            lyre.set_position(42, 28)
        lyre.lock_position()
        lyre.set_position(42, 28)
        self.assertFalse(lyre.test_position())
        lyre.unlock_position()
        self.assertEqual(dmx.set.call_count, 2)
        self.assertEqual(dmx.set.call_args_list[0][0], (42+CHANNEL.pan.value-1, 42))
        self.assertEqual(dmx.set.call_args_list[1][0], (42+CHANNEL.tilt.value-1, 28))
        self.assertEqual(lyre.get_position(), (42, 28)) 
 
    def test_gobo(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_gobo(GOBO.flower)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.gobo.value-1, GOBO.flower.value))
        self.assertEqual(lyre.gobo, GOBO.flower) 
 
    def test_color(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_color(COLOR.green)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.color.value-1, COLOR.green.value))
        self.assertEqual(lyre.color, COLOR.green) 
 
    def test_dimmer(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_dimmer(58)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.dimmer.value-1, 58))
        self.assertEqual(lyre.dimmer, 58) 
 
    def test_strombo(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_strombo(58)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.strombo.value-1, 58))
        self.assertEqual(lyre.strombo, 58) 
 
    def test_speed(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_speed(58)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.speed.value-1, 58))
        self.assertEqual(lyre.speed, 58) 
 
    def test_speed_motor(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.set_speed_motor(58)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.speed_motor.value-1, 58))
        self.assertEqual(lyre.speed_motor, 58) 

    def test_reload(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        lyre.connect()
        lyre.lock_position()
        lyre.set_position(12,13)
        lyre.set_color(COLOR.orange)
        lyre.set_gobo(GOBO.dots)
        lyre.set_dimmer(42)
        lyre.set_speed(15)
        lyre.set_speed_motor(16)
        lyre.set_strombo(17)
        lyre.disconnect()
        lyre.unlock_position()
        relay, dmx = Mock(), Mock()
        lyre2 = Lyre("test2", relay, 42, dmx)
        lyre2.reload(lyre)
        self.assertEqual(lyre2.get_position(), lyre.get_position())
        self.assertEqual(lyre2.color, lyre.color)
        self.assertEqual(lyre2.gobo, lyre.gobo)
        self.assertEqual(lyre2.dimmer, lyre.dimmer)
        self.assertEqual(lyre2.speed, lyre.speed)
        self.assertEqual(lyre2.speed_motor, lyre.speed_motor)
        self.assertEqual(lyre2.strombo, lyre.strombo)

    def test_eq(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        self.assertEqual(lyre, lyre)
        self.assertNotEqual(lyre, 12)
        lyre2 = Lyre("test", relay, 42, dmx)
        self.assertEqual(lyre, lyre2)
        lyre2.connect()
        lyre2.lock_position()
        lyre2.set_position(12, 0)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_position(0, 12)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_position(0, 0)
        self.assertEqual(lyre, lyre2)

        lyre2.set_color(COLOR.green)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_color(COLOR.white)
        self.assertEqual(lyre, lyre2)

        lyre2.set_gobo(GOBO.flake)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_gobo(GOBO.simple_round)
        self.assertEqual(lyre, lyre2)

        lyre2.set_speed(12)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_speed(0)
        self.assertEqual(lyre, lyre2)

        lyre2.set_speed_motor(12)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_speed_motor(0)
        self.assertEqual(lyre, lyre2)

        lyre2.set_dimmer(12)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_dimmer(0)
        self.assertEqual(lyre, lyre2)

        lyre2.set_strombo(12)
        self.assertNotEqual(lyre, lyre2)
        lyre2.set_strombo(0)
        self.assertEqual(lyre, lyre2)

    def test_str(self, sleep):
        relay, dmx = Mock(), Mock()
        lyre = Lyre("test", relay, 42, dmx)
        self.assertTrue("Lyre" in str(lyre))


