import unittest
from mock import patch, MagicMock
import threading
from time import sleep, time
import pytest
from parametrize import parametrize
from data_manager.read_tree.configure_tree import config_tree
from data_manager.utils.Getter import Getter
from data_manager.read_tree.reload_tree import reload_tree
from threading import Condition
from tree.Tree import Tree

class Test_reload(unittest.TestCase):
    maxDiff = None


    def init(self, lednet):
        self.tree = Tree()
        self.manager = MagicMock()
        self.getter = Getter(self.tree, self.manager)
        config_tree(self.getter, path="tests/integration/tree/datas")
        self.env = self.tree.get_env("global")
        self.led = self.env.get_object("led_1")
        self.preset = self.env.get_preset("preset_1")
        self.scenar_on = self.env.get_scenar("allumer", "preset_1")

    @parametrize("inter", [0, 1, 2 ,3]) 
    @patch("data_manager.read_tree.configure_object.LEDnet")
    def test_no_change(self, lednet, inter):
        self.init(lednet)
        if inter == 1:
            self.tree.press_inter("global", "inter_1", None)
        elif inter == 2:
            self.tree.change_mode("mode_2")
        elif inter == 3:
            self.tree.change_mode("mode_2")
            self.tree.press_inter("global", "inter_1", None)
            sleep(3)
        reload_tree(self.getter, path="tests/integration/tree/datas")
        self.assertNotEqual(self.tree, self.getter.get_tree())
        self.assertEqual(str(self.tree), str(self.getter.get_tree()))

    @patch("data_manager.read_tree.configure_object.LEDnet")
    def test_change_color(self, lednet):
        self.init(lednet)
        self.tree.press_inter("global", "inter_1", None)

        reload_tree(self.getter, path="tests/integration/tree/datas2")
        self.assertNotEqual(self.tree, self.getter.get_tree())
        for line1, line2 in zip(str(self.tree).split("\n"), str(self.getter.get_tree()).split("\n")):
            if line1 != line2:
                self.assertIn("0xffffff", line2)
                self.assertIn("0xff0000", line1)



