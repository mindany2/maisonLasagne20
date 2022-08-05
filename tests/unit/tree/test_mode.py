import unittest
from tree.Mode import Mode
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestMode(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.name, self.scenar_init, self.scenar_end = str(Mock()), Mock(), Mock()
        self.mode = Mode(self.name, self.scenar_init, self.scenar_end)

    def test_add_inter(self):
        name_inter = Mock()
        self.mode.add_inter(name_inter)
        self.assertTrue(name_inter in self.mode.get_inters())

    def test_initialize(self):
        self.mode.initialize()
        self.assertEqual(self.scenar_init.get_scenarios.call_count, 1)
        self.assertEqual(self.scenar_end.get_scenarios.call_count, 1)
        self.assertEqual(self.scenar_init.get_scenarios().initialize.call_count, 1)
        self.assertEqual(self.scenar_end.get_scenarios().initialize.call_count, 1)

    def test_change_state(self):
        self.assertFalse(self.mode.get_state())
        self.mode.change_state(True)
        self.assertEqual(self.scenar_init.get_scenarios().do.call_count, 0)
        self.mode.initialize()
        self.mode.change_state(True)
        self.assertEqual(self.scenar_init.get_scenarios().do.call_count, 1)
        self.assertTrue(self.scenar_init.get_scenarios().do.call_args[1]["join"])
        self.assertEqual(self.scenar_end.get_scenarios().do.call_count, 0)

        self.mode.change_state(False)
        self.assertEqual(self.scenar_init.get_scenarios().do.call_count, 1)
        self.assertEqual(self.scenar_end.get_scenarios().do.call_count, 1)
        self.assertTrue(self.scenar_end.get_scenarios().do.call_args[1]["join"])

    def test_str(self):
        self.assertTrue(self.name in str(self.mode))
        self.assertTrue(str(self.scenar_init) in str(self.mode))
        self.assertTrue(str(self.scenar_end) in str(self.mode))
 
