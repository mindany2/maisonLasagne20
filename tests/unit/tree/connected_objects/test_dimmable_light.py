import unittest
from tree.connected_objects.Dimmable_light import Dimmable_light, BULD
from tree.utils.Locker import Locker
from In_out.external_boards.Triak import STATE_TRIAK
from unittest.mock import Mock

class TestBULD(unittest.TestCase):
    def test_init(self):
        for name in BULD:
            self.assertEqual(len(name.value), 2)

class TestDimmableLight(unittest.TestCase):
    def test_init(self):
        triak = Mock()
        Dimmable_light("test", triak, BULD.buld_63)
        self.assertEqual(triak.set.call_count, 1)
        self.assertGreater(triak.set.call_args[0][0], 10**4)
        self.assertEqual(triak.set.call_args[0][1], STATE_TRIAK.off)

    def test_connect(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        self.assertTrue(light.connect())
        self.assertEqual(triak.set.call_count, 2)
        self.assertEqual(triak.set.call_args[0][0], 400)

        light.set_dimmer(100)
        self.assertEqual(triak.set.call_count, 3)
        self.assertEqual(triak.set.call_args[0][0], 80)

        self.assertTrue(light.connect())
        self.assertEqual(triak.set.call_count, 4)
        self.assertEqual(triak.set.call_args[0][0], 80)

    def test_disconnect(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        light.disconnect()
        self.assertEqual(triak.set.call_count, 2)
        self.assertGreater(triak.set.call_args[0][0], 10**4)
        self.assertEqual(triak.set.call_args[0][1], STATE_TRIAK.off)
        light.set_dimmer(100)
        light.disconnect()
        self.assertEqual(triak.set.call_count, 4)
        self.assertGreater(triak.set.call_args[0][0], 10**4)
        self.assertEqual(triak.set.call_args[0][1], STATE_TRIAK.on)

    def test_set_dimmer(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        light.set_dimmer(20)
        self.assertEqual(light.dimmer, 20)
        self.assertEqual(triak.set.call_count, 2)
        self.assertEqual(triak.set.call_args[0][0], 336)

    def test_reload(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        light.set_dimmer(20)
        triak2 = Mock()
        light2 = Dimmable_light("test", triak2, BULD.buld_200)
        light2.reload(light)
        self.assertTrue(light2.dimmer, 20)
        self.assertEqual(triak.set.call_count, 2)
        self.assertEqual(triak2.set.call_count, 1)

    def test_equals(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        light2 = Dimmable_light("test", triak, BULD.buld_63)
        self.assertEqual(light, light2)
        light2 = Dimmable_light("test ", triak, BULD.buld_63)
        self.assertNotEqual(light, light2)
        light2 = Dimmable_light("test", triak, BULD.buld_200)
        self.assertNotEqual(light, light2)
        triak2 = Mock()
        light2 = Dimmable_light("test", triak2, BULD.buld_200)
        self.assertNotEqual(light, light2)
        self.assertNotEqual(light, 42)

    def test_string(self):
        triak = Mock()
        light = Dimmable_light("test", triak, BULD.buld_63)
        self.assertTrue(str(light).count(str(id(triak))))
        self.assertTrue(str(light).count("test"))
        self.assertTrue(str(light).count("buld_63"))

        


