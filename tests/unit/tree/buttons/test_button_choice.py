import unittest
from tree.buttons.Button_choice import Button_choice
from unittest.mock import Mock
from mock import patch

class TestButtonChoice(unittest.TestCase):
    def test_press(self):
        manager = Mock()
        list_scenar = [Mock(), Mock(), Mock(), Mock()]
        button = Button_choice("test", manager, list_scenar)
        for i in range(len(list_scenar[:-1])):
            manager.get_current_scenar.return_value = list_scenar[i]
            button.press()
            self.assertGreater(manager.get_current_scenar.call_count, 0)
            self.assertEqual(manager.do_scenar_principal.call_count, i+1)
            self.assertEqual(manager.do_scenar_principal.call_args[0][0], list_scenar[i+1])

        manager.get_current_scenar.return_value = list_scenar[3]
        button.press(False)
        self.assertGreater(manager.get_current_scenar.call_count, 0)
        self.assertEqual(manager.do_scenar_principal.call_count, i+2)
        self.assertEqual(manager.do_scenar_principal.call_args[0][0], list_scenar[0])

    def test_eq(self):
        manager = Mock()
        list_scenar = [Mock(), Mock(), Mock(), Mock()]
        button = Button_choice("test", manager, list_scenar)
        button1 = Button_choice("test", manager, list_scenar.copy())
        self.assertEqual(button, button1)
        self.assertEqual(button, button)
        self.assertNotEqual(45, button)
        button1 = Button_choice("test", manager, [Mock()])
        self.assertNotEqual(button, button1)

    def test_str(self):
        manager = Mock()
        list_scenar = [Mock(), Mock(), Mock(), Mock()]
        button = Button_choice("test", manager, list_scenar)
        self.assertTrue("choice" in str(button))
        for scenar in list_scenar:
            self.assertTrue(str(scenar.name) in str(button))

