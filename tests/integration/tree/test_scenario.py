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

config_tree(getter, path="tests/integration/tree/datas")

env = tree.get_env("global")
preset = env.get_preset("preset_1")
scenar_on = env.get_scenar("allumer", "preset_1")
scenar_off = env.get_scenar("eteindre", "preset_1")

class TestScenario(unittest.TestCase):

    def test_init(self):
        self.assertTrue(scenar_off.state())
        self.assertFalse(scenar_on.state())


