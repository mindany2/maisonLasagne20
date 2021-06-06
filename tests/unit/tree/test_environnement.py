import unittest
from tree.Environnement import Environnement, Calculator, MARKER
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestEnvironnement(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.name = "test"
        self.env = Environnement(self.name)

    def test_add_sub_env(self):
        self.sub_env = Mock()
        self.env.add_env(self.sub_env)
        self.assertTrue(self.sub_env in self.env.get_list_subs_env())

    def test_add_preset(self):
        self.preset = Mock()
        self.env.add_preset(self.preset)
        self.assertTrue(self.preset in self.env.get_list_presets())

    def test_add_object(self):
        self.obj = Mock()
        self.env.add_object(self.obj)
        self.assertTrue(self.obj in self.env.get_list_objs())
        self.assertTrue(self.env.get_object(self.obj.name))
        with self.assertRaises(KeyError):
            self.env.get_object("test")

    def test_add_mode(self):
        self.preset = Mock()
        self.env.add_preset(self.preset)
        self.mode = Mock()
        self.env.add_mode(self.mode, self.preset)
        self.assertTrue(self.mode in self.env.list_presets_chosen.keys())
        self.assertTrue(self.preset in self.env.list_presets_chosen)


    @parametrize("recursive", [False, True])
    @patch.object(Calculator, "add")
    @patch.object(Calculator, "get")
    def test_add_variable(self, get, add, recursive):
        self.sub_env1, self.sub_env2 = Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.var = Mock()
        self.assertTrue(isinstance(self.env.get_calculator(), Calculator))
        self.env.add_variable(self.var, recursive=recursive)
        self.assertEqual(add.call_count, 1)
        self.assertEqual(add.call_args[0][0], self.var)
        
        self.assertEqual(self.sub_env1.add_variable.call_count, int(recursive))
        self.assertEqual(self.sub_env2.add_variable.call_count, int(recursive))
        if recursive:
            self.assertEqual(self.sub_env1.add_variable.call_args[0][0], self.var)
            self.assertEqual(self.sub_env2.add_variable.call_args[0][0], self.var)

        self.assertTrue(self.env.get_var(self.var.name))
        self.assertEqual(get.call_count, 1)
        self.assertEqual(get.call_args[0][0], self.var.name)
        def raise_get(name):
            raise KeyError
        get.side_effect = raise_get
        with self.assertRaises(KeyError):
            self.env.get_var("test")

    def test_preset_select(self):
        self.preset1, self.preset2, self.preset3 = Mock(), Mock(), Mock()
        self.env.add_preset(self.preset1)
        self.env.add_preset(self.preset2)
        self.env.add_preset(self.preset3)
        self.assertEqual(self.env.get_preset_select(), self.preset1)
        self.env.change_preset_select(self.preset3)
        self.assertEqual(self.env.get_preset_select(), self.preset3)
        self.assertFalse(self.env.state())
        self.preset3.get_marker.return_value = MARKER.ON
        self.assertTrue(self.env.state())

    def test_is_on(self):
        self.sub_env1, self.sub_env2 = Environnement("sub_env1"), Environnement("sub_env2")
        self.preset, self.preset1, self.preset2 = Mock(), Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.env.add_preset(self.preset)
        self.sub_env1.add_preset(self.preset1)
        self.sub_env2.add_preset(self.preset2)

        self.assertFalse(self.env.is_on())
        self.preset.get_marker.return_value = MARKER.ON
        self.assertTrue(self.env.is_on())
        self.preset.get_marker.return_value = MARKER.OFF
        self.preset2.get_marker.return_value = MARKER.ON
        self.assertTrue(self.env.is_on())

    @parametrize("marker", [MARKER.OFF, MARKER.ON, MARKER.DECO])
    @patch.object(Calculator, "reset")
    def test_change_mode(self, reset, marker):
        self.sub_env1, self.sub_env2 = Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.preset, self.preset1, self.preset2 = Mock(), Mock(), Mock()
        self.mode, self.mode1, self.mode2 = Mock(), Mock(), Mock()
        self.env.add_preset(self.preset)
        self.env.add_preset(self.preset1)
        self.env.add_preset(self.preset2)
        self.env.add_mode(self.mode.name, self.preset)
        self.env.add_mode(self.mode1.name, self.preset1)
        self.env.add_mode(self.mode2.name, self.preset2)

        self.preset.get_marker.return_value = marker

        self.env.change_mode(Mock())
        self.env.change_mode(self.mode1)
        self.assertEqual(self.sub_env1.change_mode.call_count, 2)
        self.assertEqual(self.sub_env2.change_mode.call_count, 2)
        self.assertEqual(self.sub_env1.change_mode.call_args[0][0], self.mode1)
        self.assertEqual(self.sub_env2.change_mode.call_args[0][0], self.mode1)

        self.assertEqual(reset.call_count, 1)
        self.assertEqual(self.preset.reset.call_count, 1)
        self.assertEqual(self.preset1.initialize.call_count, 1)
        if marker == MARKER.DECO:
            marker = MARKER.OFF
        self.assertEqual(self.preset1.initialize.call_args[0][0], marker)
        self.assertEqual(self.env.get_preset_select(), self.preset1)

    def test_do_current_scenar(self):
        self.sub_env1, self.sub_env2 = Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.preset = Mock()
        self.env.add_preset(self.preset)
        self.env.do_current_scenar()
        self.assertEqual(self.sub_env1.do_current_scenar.call_count, 1)
        self.assertEqual(self.sub_env2.do_current_scenar.call_count, 1)
        self.assertEqual(self.preset.do_current_scenar.call_count, 1)

    def test_get_preset(self):
        self.preset, self.preset1, self.preset2 = Mock(), Mock(), Mock()
        self.env.add_preset(self.preset)
        self.env.add_preset(self.preset1)
        self.env.add_preset(self.preset2)

        self.assertEqual(self.env.get_preset(self.preset1.name), self.preset1)
        with self.assertRaises(KeyError):
            self.env.get_preset("lol")

    def test_get_env(self):
        self.sub_env, self.sub_env1, self.sub_env2 = Environnement("test"), Environnement("test1"), Environnement("test2")
        self.env.add_env(self.sub_env)
        self.env.add_env(self.sub_env1)
        self.sub_env1.add_env(self.sub_env2)
        self.assertEqual(self.env.get_env(["test"]), self.sub_env)
        self.assertEqual(self.env.get_env(["test1", "test2"]), self.sub_env2)
        with self.assertRaises(KeyError):
            self.env.get_env("lol")

        liste = self.env.get_list_envs()
        self.assertEqual(liste.get(self.env.name), self.env)
        self.assertEqual(liste.get(f"{self.env.name}.test"), self.sub_env)
        self.assertEqual(liste.get(f"{self.env.name}.test1"), self.sub_env1)
        self.assertEqual(liste.get(f"{self.env.name}.test1.test2"), self.sub_env2)

    @parametrize("preset", [None, Mock()])
    def test_get_scenar(self, preset):
        self.preset_select = Mock()
        self.env.add_preset(self.preset_select)
        if preset:
            self.env.add_preset(preset)

        self.assertEqual(self.env.get_preset_select(), self.preset_select)
        name = "lol"
        if preset:
            scenar = self.env.get_scenar(name, preset=preset.name)
        else:
            scenar = self.env.get_scenar(name)
        if preset:
            self.assertEqual(preset.get_scenar.call_count, 1)
            self.assertEqual(preset.get_scenar.call_args[0][0], name)
            self.assertEqual(scenar, preset.get_scenar())
        else:
            self.assertEqual(self.preset_select.get_scenar.call_count, 1)
            self.assertEqual(self.preset_select.get_scenar.call_args[0][0], name)
            self.assertEqual(scenar, self.preset_select.get_scenar())
        def raise_(name):
            raise KeyError()

        self.preset_select.get_scenar.side_effect = raise_
        if preset:
            preset.get_scenar.side_effect = raise_

        with self.assertRaises(KeyError):
            self.env.get_scenar("lol")

    def test_press_inter(self):
        self.sub_env1, self.sub_env2 = Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.preset, self.preset1 = Mock(), Mock()
        self.env.add_preset(self.preset)
        self.env.add_preset(self.preset1)
        self.env.change_preset_select(self.preset1)
        name, state = Mock(), Mock()
        self.env.press_inter(name, state)
        self.assertEqual(self.preset1.press_inter.call_count, 1)
        self.assertEqual(self.sub_env1.press_inter.call_count, 1)
        self.assertEqual(self.sub_env2.press_inter.call_count, 1)
        self.assertEqual(self.preset1.press_inter.call_args[0], (name, state))
        self.assertEqual(self.sub_env1.press_inter.call_args[0], (name, state))
        self.assertEqual(self.sub_env2.press_inter.call_args[0], (name, state))

    def test_initialize(self):
        self.sub_env1, self.sub_env2 = Mock(), Mock()
        self.env.add_env(self.sub_env1)
        self.env.add_env(self.sub_env2)
        self.preset, self.preset1 = Mock(), Mock()
        self.env.add_preset(self.preset)
        self.env.add_preset(self.preset1)
        self.env.change_preset_select(self.preset1)
        self.env.initialize()
        self.assertEqual(self.preset1.initialize.call_count, 1)
        self.assertEqual(self.sub_env1.initialize.call_count, 1)
        self.assertEqual(self.sub_env2.initialize.call_count, 1)

    def test_str(self):
        self.assertTrue(self.name in str(self.env))











 
