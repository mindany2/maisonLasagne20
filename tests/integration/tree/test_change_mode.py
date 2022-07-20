import unittest
from mock import patch, MagicMock
import threading
from time import sleep, time
import pytest
from parametrize import parametrize
from data_manager.read_tree.configure_tree import config_tree
from data_manager.utils.Getter import Getter
from threading import Condition
from tree.Tree import Tree

tree = Tree()
manager = MagicMock()
getter = Getter(tree, manager)

with patch("data_manager.read_tree.configure_object.LEDnet") as lednet:
    config_tree(getter, path="tests/integration/tree/datas")

controller = lednet.return_value
env = tree.get_env("global")
led = env.get_object("led_1")
preset_1 = env.get_preset("preset_1")
scenar1_on = env.get_scenar("allumer", "preset_1")
scenar1_off = env.get_scenar("eteindre", "preset_1")
preset_2 = env.get_preset("preset_2")
scenar2_on = env.get_scenar("allumer", "preset_2")
scenar2_off = env.get_scenar("eteindre", "preset_2")

class Test_change_mode(unittest.TestCase):

    def test_change_mode(self):
        cond = Condition()
        def disconnect(is_black=False):
            with cond:
                cond.notify()

        controller.disconnect.side_effect = disconnect
        tree.press_inter("global", "inter_1", True)
        self.assertTrue(scenar1_on.state())
        self.assertEqual(tree.get_current_mode(), tree.get_mode("mode_1"))
        tree.change_mode("mode_2")
        self.assertEqual(tree.get_current_mode(), tree.get_mode("mode_2"))
        self.assertFalse(scenar1_on.state())
        self.assertTrue(scenar2_on.state())

        with cond:
            cond.wait()

        self.assertEqual(controller.disconnect.call_count, 1)
        self.assertEqual(str(controller.send_color.call_args[0][0]), "0x00004C")
 
        tree.change_mode("mode_1")
        self.assertEqual(tree.get_current_mode(), tree.get_mode("mode_1"))
        self.assertFalse(scenar2_on.state())
        self.assertTrue(scenar1_on.state())

        with cond:
            cond.wait()

        self.assertEqual(str(controller.send_color.call_args[0][0]), "0x7F0000")
 

