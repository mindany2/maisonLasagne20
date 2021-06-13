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

COLORS = ['0x000000', '0x000000', '0x010000', '0x020000', '0x050000', '0x070000', '0x0B0000', '0x0F0000', '0x140000', '0x190000', '0x1F0000', '0x260000', '0x2D0000', '0x350000', '0x3E0000', '0x470000', '0x510000', '0x5B0000', '0x670000', '0x720000', '0x7F0000', '0x7F0000', '0x7F0000', '0x7F0606', '0x7F0C0C', '0x7F1313', '0x7F1919', '0x7F1F1F', '0x7F2626', '0x7F2C2C', '0x7F3333', '0x7F3939', '0x7F3F3F', '0x7F4646', '0x7F4C4C', '0x7F5252', '0x7F5959', '0x7F5F5F', '0x7F6666', '0x7F6C6C', '0x7F7272', '0x7F7979', '0x7F7F7F']

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
        self.scenar_off = self.env.get_scenar("eteindre", "preset_1")

    @parametrize("inter", [0, 1, 2 ,3]) 
    @patch("data_manager.read_tree.configure_object.LEDnet")
    def test_no_change(self, lednet, inter):
        self.init(lednet)
        controller = lednet.return_value
        self.cond = threading.Condition()
        self.colors = []

        def disconnect(is_black=None):
            with self.cond:
                self.cond.notify()
        controller.disconnect.side_effect = disconnect

        if inter == 1:
            self.tree.press_inter("global", "inter_1", None)
            with self.cond:
                self.cond.wait()
        elif inter == 2:
            self.tree.change_mode("mode_2")
        elif inter == 3:
            self.tree.change_mode("mode_2")
            self.tree.press_inter("global", "inter_1", None)
            with self.cond:
                self.cond.wait()
        reload_tree(self.getter, path="tests/integration/tree/datas")
        self.assertNotEqual(self.tree, self.getter.get_tree())
        self.assertEqual(str(self.tree), str(self.getter.get_tree()))

    @patch("data_manager.read_tree.configure_object.LEDnet")
    def test_change_color(self, lednet):
        self.init(lednet)
        controller = lednet.return_value
        self.cond = threading.Condition()
        self.colors = []

        def disconnect(is_black=None):
            with self.cond:
                self.cond.notify()

        def set_color(color):
            self.colors.append(str(color))

        controller.send_color.side_effect = set_color
        controller.disconnect.side_effect = disconnect

        self.tree.press_inter("global", "inter_1", None)
        with self.cond:
            self.cond.wait()

        reload_tree(self.getter, path="tests/integration/tree/datas2")
        self.assertNotEqual(self.tree, self.getter.get_tree())
        for line1, line2 in zip(str(self.tree).split("\n"), str(self.getter.get_tree()).split("\n")):
            if line1 != line2:
                self.assertIn("0xffffff", line2)
                self.assertIn("0xff0000", line1)
        with self.cond:
            self.cond.wait()

        self.assertEqual(self.colors, COLORS)



