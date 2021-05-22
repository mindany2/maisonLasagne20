import unittest
from tree.connected_objects.dmx.Crazy_2 import Crazy_2, CHANNEL
from unittest.mock import Mock
from mock import patch

class TestCrazy2(unittest.TestCase):
    def test_init(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 0, dmx)
        self.assertEqual(crazy.program, 0)
        self.assertEqual(crazy.speed, 0)
        self.assertEqual(crazy.strombo, 0)

    def test_set_program(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 42, dmx)
        crazy.connect()
        crazy.set_program(135)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.program.value-1, 135))
        self.assertEqual(crazy.program, 135)

    def test_set_speed(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 42, dmx)
        crazy.connect()
        crazy.set_speed(15235)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.speed.value-1, 15235))
        self.assertEqual(crazy.speed, 15235)

    def test_set_strombo(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 42, dmx)
        crazy.connect()
        crazy.set_strombo(15235)
        self.assertEqual(dmx.set.call_count, 1)
        self.assertEqual(dmx.set.call_args[0], (42+CHANNEL.strombo.value-1, 15235))
        self.assertEqual(crazy.strombo, 15235)

    def test_reload(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 42, dmx)
        crazy.connect()
        crazy.set_strombo(15)
        crazy.set_program(42)
        crazy.set_speed(185)

        crazy2 = Crazy_2("test", Mock(), 85, Mock())
        crazy2.reload(crazy)
        self.assertEqual(crazy.program, crazy2.program)
        self.assertEqual(crazy.speed, crazy2.speed)
        self.assertEqual(crazy.strombo, crazy2.strombo)

    def test_eq(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 42, dmx)
        self.assertEqual(crazy, crazy)
        self.assertNotEqual(crazy, None)
        crazy2 = Crazy_2("test ", relay, 42, dmx)
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", relay, 12, dmx)
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", Mock(), 42, dmx)
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", relay, 42, Mock())
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", relay, 42, dmx)
        crazy2.connect()
        crazy2.set_program(12)
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", relay, 42, dmx)
        crazy2.connect()
        crazy2.set_speed(12)
        self.assertNotEqual(crazy, crazy2)
        crazy2 = Crazy_2("test", relay, 42, dmx)
        crazy2.connect()
        crazy2.set_strombo(12)
        self.assertNotEqual(crazy, crazy2)

    def test_str(self):
        relay, dmx = Mock(), Mock()
        crazy = Crazy_2("test", relay, 123456, dmx)
        self.assertTrue("test" in str(crazy))
        self.assertTrue(str(id(relay)) in str(crazy))
        self.assertTrue(str(id(dmx)) in str(crazy))
        self.assertTrue(str(123456) in str(crazy))



