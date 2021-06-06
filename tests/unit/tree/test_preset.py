import unittest
from tree.Preset import Preset, Scenario_manager, MARKER
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestPreset(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.name, self.name_env = str(Mock()), str(Mock())
        self.preset = Preset(self.name, self.name_env)
    
    @patch.object(Scenario_manager, "__init__", return_value=None)
    def test_init(self, manager):
        self.preset = Preset(self.name, self.name_env)
        self.assertEqual(manager.call_count, 1)
        self.assertEqual(manager.call_args[0][0], f"{self.name_env}.{self.name}")

    def test_add_button(self):
        self.button = Mock()
        self.preset.add_button(self.button)
        self.assertTrue(self.button in self.preset.get_buttons())
        self.assertEqual(self.preset.get_button(self.button.name), self.button)
    
    def test_press_inter(self):
        self.button = Mock()
        self.preset.add_button(self.button)
        self.preset.press_inter("lol", 0)
        self.assertEqual(self.button.press.call_count, 0)
        self.preset.press_inter(self.button.name, 42)
        self.assertEqual(self.button.press.call_count, 1)
        self.assertEqual(self.button.press.call_args[0][0], 42)

    def test_change_state(self):
        self.assertFalse(self.preset.state)
        self.preset.change_state(True)
        self.assertTrue(self.preset.state)

    def test_add_scenario(self):
        self.scenar = Mock()
        self.preset.add_scenar(self.scenar)
        self.assertTrue(self.scenar in self.preset.get_list_scenars())
        self.assertEqual(self.preset.get_scenar(self.scenar.name), self.scenar)

    @patch.object(Scenario_manager, "get_marker")
    @patch.object(Scenario_manager, "reset")
    def test_manager(self, reset, marker):
        self.assertTrue(isinstance(self.preset.get_manager(), Scenario_manager))
        self.assertEqual(self.preset.get_marker(), marker.return_value)
        self.preset.reset()
        self.assertEqual(reset.call_count, 1)

    @parametrize("marker,marker_scenar", [(MARKER.DECO, MARKER.DECO), (MARKER.OFF, MARKER.ON), (MARKER.DECO, MARKER.OFF)])
    @patch.object(Scenario_manager, "initialize")
    def test_initialize(self, initialize, marker, marker_scenar):
        scenar, scenar1, scenar2 = Mock(), Mock(), Mock()
        scenar.get_marker.return_value = marker_scenar
        self.preset.add_scenar(scenar)
        self.preset.add_scenar(scenar1)
        self.preset.add_scenar(scenar2)
        if marker == MARKER.OFF:
            with self.assertRaises(ValueError):
                self.preset.initialize(marker)
        else:
            self.preset.initialize(marker)
            self.assertEqual(initialize.call_count, 1)
            self.assertEqual(initialize.call_args[0][0], scenar)
            self.assertEqual(scenar.initialize.call_count, 1)
            self.assertEqual(scenar1.initialize.call_count, 1)
            self.assertEqual(scenar2.initialize.call_count, 1)

    @patch.object(Scenario_manager, "do_current_scenar")
    def test_do_current_scenar(self, do):
        self.preset.do_current_scenar()
        self.assertEqual(do.call_count, 1)

    def test_reload(self):
        preset2 = Preset("lol", "mdr")
        self.preset.change_state(True)
        preset2.reload(self.preset)
        self.assertTrue(preset2.state)
        
    def test_str(self):
        scenar = Mock()
        scenar.get_marker.return_value = MARKER.OFF
        self.preset.add_scenar(scenar)
        self.preset.initialize(MARKER.OFF)
        self.assertTrue(self.name in str(self.preset))
        self.assertTrue(str(scenar) in str(self.preset))

    


 
