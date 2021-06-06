import unittest
from tree.buttons.Button_secondary import Button_secondary
from unittest.mock import Mock
from mock import patch

class TestButtonSecondary(unittest.TestCase):

    def test_press(self):
        manager, scenar = Mock(), Mock()
        button = Button_secondary("test", manager, scenar)
        button.press()
        self.assertEqual(manager.do_scenar_secondary.call_count, 1)
        self.assertEqual(manager.do_scenar_secondary.call_args[0][0], scenar)
        button.press(False)
        self.assertEqual(manager.do_scenar_secondary.call_count, 1)
        self.assertEqual(manager.remove.call_count, 1)
        self.assertEqual(manager.remove.call_args[0][0], scenar)

    def test_state(self):
        manager, scenar = Mock(), Mock()
        button = Button_secondary("test", manager, scenar)
        self.assertEqual(button.state(), scenar.state())

    def test_eq(self):
        manager, scenar = Mock(), Mock()
        button = Button_secondary("test", manager, scenar)
        self.assertEqual(button, button)
        self.assertNotEqual(button, 5)
        button2 = Button_secondary("test", manager, Mock())
        self.assertNotEqual(button, button2)
 
    def test_str(self):
        manager, scenar = Mock(), Mock()
        button = Button_secondary("test", manager, scenar)
        self.assertTrue("secondary" in str(button))
        self.assertTrue(str(scenar.name) in str(button))
