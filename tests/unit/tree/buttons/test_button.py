import unittest
from tree.buttons.Button import Button
from unittest.mock import Mock
from mock import patch

class TestButton(unittest.TestCase):
    def test_init(self):
        Button("test")
        manager = Mock()
        button = Button("test", manager)
        button.press()

    def test_state(self):
        button = Button("test")
        self.assertFalse(button.state())


    def test_str(self):
        button = Button("test")
        self.assertTrue("test" in str(button))

    def test_eq(self):
        button = Button("test")
        button2 = Button("test2")
        self.assertEqual(button, button)
        self.assertNotEqual(button, 12)
        self.assertNotEqual(button, button2)



