import unittest
from tree.connected_objects.Connected_object import Connected_object
from tree.utils.Locker import Locker
from unittest.mock import Mock

class TestConnectedObject(unittest.TestCase):
    def test_init(self):
        obj = Connected_object("lol")
        self.assertTrue(isinstance(obj, Locker))
        self.assertEqual(obj.name, "lol")
        self.assertEqual(str(obj).count("lol"),1)

    def test_equals(self):
        obj1 = Connected_object("xd")
        obj2 = Connected_object(" xd")
        obj3 = Connected_object("xd")
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj1, obj3)
        self.assertNotEqual(obj1, 8)

    def test_repair(self):
        obj = Connected_object("lol")
        self.assertFalse(obj.repair())

    def test_reload(self):
        obj = Connected_object("lol")
        obj.reload(None)

    def test_str(self):
        obj = Connected_object("lol")
        self.assertTrue(str(obj).count("lol"))

