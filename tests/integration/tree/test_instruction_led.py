import unittest
from mock import patch, MagicMock
import threading
from time import sleep, time
import pytest
from parametrize import parametrize
from data_manager.read_tree.configure_tree import config_tree
from data_manager.utils.Getter import Getter
from tree.Tree import Tree

tree = Tree()
manager = MagicMock()
getter = Getter(tree, manager)

with patch("data_manager.read_tree.configure_object.LEDnet") as lednet:
    config_tree(getter, path="tests/integration/tree/datas")

controller = lednet.return_value
env = tree.get_env("global")
led = env.get_object("led_1")
preset = env.get_preset("preset_1")
scenar_on = env.get_scenar("allumer", "preset_1")
scenar_off = env.get_scenar("eteindre", "preset_1")
relay = manager.get_relay.return_value

class TestInstruction_led(unittest.TestCase):

    def test_init(self):
        self.assertEqual(manager.get_relay.call_count, 1)
        self.assertEqual(manager.get_relay.call_args[0], (1,1))
        self.assertEqual(relay, led.relay)

    def test_press(self):
        self.count = 0
        self.cond = threading.Condition()
        self.infos = []
        self.dimmer, self.is_black = 0, None
        def connect():
            return True

        def disconnect(is_black=None):
            self.is_black = is_black
            with self.cond:
                self.cond.notify()

        def set_color(color):
            self.infos.append((time(), color))
            self.count += 1

        def set_dimmer(dimmer):
            self.dimmer = dimmer

        controller.connect.side_effect = connect
        controller.send_color.side_effect = set_color
        controller.send_dimmer.side_effect = set_dimmer
        controller.disconnect.side_effect = disconnect
        tree.press_inter("global", "inter_1", None)
        self.assertEqual(threading.active_count(), 3)
        self.assertTrue(env.state())

        with self.cond:
            self.cond.wait()
        self.assertEqual(self.dimmer, 100)
        for i, (times, color) in enumerate(self.infos[:-1]):
            suiv_time, suiv_color = self.infos[i+1]

        self.assertEqual(str(controller.send_color.call_args[0][0]), "0x7F0000")
        self.assertEqual(self.count, 21)
    

 
