import unittest
from tree.buttons.Button_principal import Button_principal
from unittest.mock import Mock
from mock import patch

class TestButtonPrincipal(unittest.TestCase):

    def press(self, state, manager_state, scenar_off, solution):
        manager = Mock()
        scenar_on = Mock()
        button = Button_principal("test", manager, scenar_on, scenar_off)
        manager.get_state.return_value = manager_state
        button.press(state)
        self.assertEqual(manager.do_scenar_principal.call_count, 1)
        self.assertEqual(manager.do_scenar_principal.call_args[0][0], [scenar_off, scenar_on][solution])

    def test_press(self):
        for state in [None, True, False]:
            for manager_state in [False, True]:
                self.press(state, manager_state, Mock(), (state if (state != None) else not(manager_state)))

        for state in [None, True, False]:
            self.press(state, False, None, 1)

    def test_state(self):
        manager = Mock()
        scenar_on = Mock()
        button = Button_principal("test", manager, scenar_on)
        self.assertEqual(button.state(), manager.get_state())

    def test_eq(self):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_principal("test", manager, scenar_on, scenar_off)
        self.assertEqual(button, button)
        self.assertNotEqual(button, None)
        button2 = Button_principal("test", manager, Mock(), scenar_off)
        self.assertNotEqual(button2, button)
        button2 = Button_principal("test", manager, scenar_on, Mock())
        self.assertNotEqual(button2, button)
        button2 = Button_principal("test", manager, scenar_on, scenar_off)
        self.assertEqual(button, button2)

    def test_str(self):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_principal("test", manager, scenar_on, scenar_off)
        self.assertTrue("principal" in str(button))
        self.assertTrue(str(scenar_on.name) in str(button))
        self.assertTrue(str(scenar_off.name) in str(button))
 
