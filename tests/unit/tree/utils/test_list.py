import unittest
from tree.utils.List import List
from unittest.mock import Mock

class TestList(unittest.TestCase):
    def test_set_get(self):
        element = Mock()
        element.name = "test"
        list_test = List()
        list_test.add(element)
        self.assertEqual(list_test.get("test"), element)
        with self.assertRaises(AttributeError):
            list_test.add(None)

    def test_remove(self):
        element = Mock()
        element.name = "test"
        list_test = List()
        list_test.add(element)
        element.name = "test2"
        list_test.add(element)
        list_test.remove(element)
        self.assertEqual(list_test.get("test"), element)
        with self.assertRaises(KeyError):
            self.assertEqual(list_test.get("test2"), element)


