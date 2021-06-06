import unittest
from tree.buttons.Button_tempo import Button_tempo
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep

class TestButtonTempo(unittest.TestCase):


    @patch('time.sleep', return_value=None)
    @patch('time.time', return_value=0)
    def test_press(self, time, mock_sleep):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_tempo("test", manager, scenar_on, scenar_off, 12)
        button.press()
        self.assertEqual(manager.do_scenar_principal.call_count, 1)
        self.assertEqual(manager.do_scenar_principal.call_args[0][0], scenar_on)
        self.assertEqual(threading.active_count(), 2)
        self.assertTrue("test" in "".join(i.name for i in threading.enumerate()))
        self.assertTrue("tempo" in "".join(i.name for i in threading.enumerate()))
        time.return_value = 11
        button.press()
        self.assertEqual(threading.active_count(), 2)
        time.return_value = 13
        sleep(0.005)
        self.assertEqual(threading.active_count(), 2)
        time.return_value = 24
        sleep(0.005)
        self.assertEqual(manager.do_scenar_principal.call_count, 2)
        self.assertEqual(manager.do_scenar_principal.call_args[0][0], scenar_off)

    def test_state(self):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_tempo("test", manager, scenar_on, scenar_off, 0)
        self.assertEqual(button.state(), manager.get_state())

    def test_eq(self):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_tempo("test", manager, scenar_on, scenar_off, 0)
        button2 = Button_tempo("test", manager, scenar_on, scenar_off, 0)
        self.assertEqual(button, button2)
        self.assertNotEqual(button, 8)
        button2 = Button_tempo("test", manager, Mock(), scenar_off, 0)
        self.assertNotEqual(button, button2)
        button2 = Button_tempo("test", manager, scenar_on, Mock(), 0)
        self.assertNotEqual(button, button2)
        button2 = Button_tempo("test", manager, scenar_on, scenar_off, 12)
        self.assertNotEqual(button, button2)

    def test_str(self):
        manager = Mock()
        scenar_on, scenar_off = Mock(), Mock()
        button = Button_tempo("test", manager, scenar_on, scenar_off, 254)
        self.assertTrue(str(scenar_on.name) in str(button))
        self.assertTrue(str(scenar_off.name) in str(button))
        self.assertTrue("tempo" in str(button))
        self.assertTrue("254" in str(button))

