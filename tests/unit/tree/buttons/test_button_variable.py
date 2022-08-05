import unittest
from tree.buttons.Button_variable import Button_variable
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep

class TestButtonVariable(unittest.TestCase):

    def test_state(self):
        variable = Mock()
        button = Button_variable("test", variable)
        self.assertEqual(button.state(), variable.get())

    def test_press(self):
        variable = Mock()
        button = Button_variable("test", variable)
        button.press()
        self.assertEqual(variable.set.call_count, 0)
        button.press(42)
        self.assertEqual(variable.set.call_count, 1)
        self.assertEqual(variable.set.call_args[0][0], 42)

    def test_eq(self):
        variable = Mock()
        button = Button_variable("test", variable)
        button2 = Button_variable("test", variable)
        self.assertEqual(button, button2)
        self.assertNotEqual(button, 42)
        button2 = Button_variable("test", Mock())
        self.assertNotEqual(button, button2)

    def test_str(self):
        variable = Mock()
        button = Button_variable("test", variable)
        self.assertTrue(str(variable.name) in str(button))
        self.assertTrue("variable" in str(button))


