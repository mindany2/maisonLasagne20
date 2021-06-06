import unittest
from tree.Tree import Tree, Environnement
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestTree(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.tree = Tree()

    def test_global_env(self):
        self.assertEqual("global", self.tree.get_global_env().name)

    def test_mode(self):
        mode = Mock()
        self.tree.add_mode(mode)
        self.assertTrue(mode in self.tree.get_modes())
        self.assertEqual(self.tree.get_mode(mode.name), mode)
        with self.assertRaises(KeyError):
            self.tree.get_mode("lol")

    @patch.object(Environnement, "change_mode")
    @patch.object(Environnement, "do_current_scenar")
    def test_change_mode(self, do_current_scenar, change_mode):
        mode, mode1, mode2 = Mock(), Mock(), Mock()
        self.tree.add_mode(mode)
        self.tree.add_mode(mode1)
        self.tree.add_mode(mode2)

        self.assertEqual(self.tree.get_current_mode(), mode)
        self.tree.change_mode(mode2.name)
        self.assertEqual(self.tree.get_current_mode(), mode2)
        self.assertEqual(do_current_scenar.call_count, 1)
        self.assertEqual(change_mode.call_count, 1)
        self.assertEqual(change_mode.call_args[0][0], mode2)

    @parametrize("name", ["test", "test.test2.test3", "global.test.lol", None])
    @patch.object(Environnement, "get_env")
    def test_get_env(self, get_env, name):
        def raise_(name):
            raise KeyError
        if name:
            self.tree.get_env(name)
            self.assertEqual(get_env.call_count, 1)
            self.assertEqual(get_env.call_args[0][0], name.replace("global.","").split("."))
        else:
            get_env.side_effect = raise_
            with self.assertRaises(KeyError):
                self.tree.get_env("lol")

    @patch.object(Environnement, "get_list_envs")
    def test_get_list_envs(self, get_list_envs):
        self.assertEqual(self.tree.get_list_envs(), get_list_envs())

    @parametrize("name_env", ["test.sub_env", "mode.normal"])
    @patch.object(Tree, "change_mode")
    @patch.object(Environnement, "get_env")
    def test_press_inter(self, get_env, change_mode, name_env):
        name_inter, state = Mock(), Mock()
        self.tree.press_inter(name_env, name_inter, state)
        if "mode" in name_env:
            self.assertEqual(change_mode.call_count, 1)
            self.assertEqual(change_mode.call_args[0][0], "normal")
            self.assertEqual(get_env.call_count, 0)
        else:
            self.assertEqual(get_env.call_count, 1)
            self.assertEqual(get_env.call_args[0][0], name_env.split("."))
            self.assertEqual(get_env.return_value.press_inter.call_count, 1)
            self.assertEqual(get_env.return_value.press_inter.call_args[0], (name_inter, state))
            self.assertEqual(change_mode.call_count, 0)

    @patch.object(Environnement, "get_env")
    def test_get_scenar(self, get_env):
        name_env, name_scenar, preset = "test", Mock(), Mock()
        self.tree.get_scenar(name_env, name_scenar, preset)
        self.assertEqual(get_env.call_count, 1)
        self.assertEqual(get_env.call_args[0][0], [name_env])
        self.assertEqual(get_env.return_value.get_scenar.call_count, 1)
        self.assertEqual(get_env.return_value.get_scenar.call_args[0], (name_scenar, preset))

    @patch.object(Environnement, "initialize")
    @patch.object(Environnement, "change_mode")
    def test_initialize(self, change_mode, initialize):
        mode, mode1, mode2 = Mock(), Mock(), Mock()
        self.tree.add_mode(mode)
        self.tree.add_mode(mode1)
        self.tree.add_mode(mode2)
        self.tree.initialize()
        self.assertEqual(mode.initialize.call_count, 1)
        self.assertEqual(mode1.initialize.call_count, 1)
        self.assertEqual(mode2.initialize.call_count, 1)
        self.assertEqual(initialize.call_count, 1)
        self.assertEqual(change_mode.call_count, 1)
        self.assertEqual(change_mode.call_args[0][0], mode)

    def test_str(self):
        mode, mode1, mode2 = Mock(), Mock(), Mock()
        self.tree.add_mode(mode)
        self.tree.add_mode(mode1)
        self.tree.add_mode(mode2)
        self.assertTrue(str(mode) in str(self.tree))
        self.assertTrue(str(mode1) in str(self.tree))
        self.assertTrue(str(mode2) in str(self.tree))
        self.assertTrue("Thread" in str(self.tree))
        self.assertTrue("Tree" in str(self.tree))





        


