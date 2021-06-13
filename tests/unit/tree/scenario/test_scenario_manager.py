import unittest
from tree.scenario.Scenario_manager import Scenario_manager, MARKER, Lock
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestScenarioManager(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.name = "test"
        self.manager = Scenario_manager(self.name)
        self.scenar_init = Mock()
        self.mutex = Mock()
        self.manager.mutex = self.mutex

    def test_initialize(self):
        self.manager.initialize(self.scenar_init)
        self.assertEqual(self.manager.get_current_scenar(), self.scenar_init)
        self.assertEqual(self.manager.get_scenar_select(), self.scenar_init)

    @parameterized.expand(((True,), (False,)))
    def test_do_current(self, state):
        with self.assertRaises(AssertionError):
            self.manager.do_current_scenar()
        self.manager.initialize(self.scenar_init)
        self.scenar_init.state.return_value = state
        self.manager.do_current_scenar()
        self.assertEqual(self.scenar_init.do.call_count, 2)
        self.assertEqual(self.scenar_init.set_state.call_count, 2)
        if not state:
            self.assertEqual(self.scenar_init.set_state.call_args[0][0], not state)
        self.assertEqual(self.mutex.acquire.call_count, 2)
        self.assertEqual(self.mutex.release.call_count, 2)

    def test_do_principal_no_initialize(self):
        self.manager.do_scenar_principal(self.scenar_init)
        self.assertEqual(self.mutex.acquire.call_count, 1)
        self.assertEqual(self.mutex.release.call_count, 1)
        self.assertEqual(self.scenar_init.do.call_count, 0)
        self.assertEqual(self.mutex.release.call_count, 1)

    @parameterized.expand(((MARKER.DECO, None), (MARKER.NONE, None), (MARKER.OFF, MARKER.DECO),
                        (MARKER.OFF, MARKER.ON), (MARKER.OFF, MARKER.OFF), (MARKER.ON,None)))
    def test_do_principal(self, marker, marker_init):
        self.manager.initialize(self.scenar_init)
        self.scenar = Mock()
        self.scenar.get_marker.return_value = marker
        self.scenar_init.get_marker.return_value = marker_init
        self.scenar_stack = Mock()
        if marker_init != MARKER.DECO:
            self.manager.push(self.scenar_stack)
            self.manager.push(self.scenar_stack)
        self.manager.do_scenar_principal(self.scenar)
        if marker == MARKER.NONE:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar_init)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar_init)
        elif marker != MARKER.OFF or marker_init == MARKER.OFF:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar)
            self.assertEqual(self.scenar.do.call_count, 1)
            if marker_init == MARKER.OFF:
                self.assertFalse(self.manager.get_stack())
            else:
                self.assertEqual(self.manager.get_stack(), [self.scenar_stack]*2)
        elif marker_init != MARKER.DECO:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar_stack)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar)
            self.assertEqual(self.scenar_stack.do.call_count, 1)
            self.assertEqual(self.manager.get_stack(), [self.scenar_stack]*2)
        else:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar)
            self.assertEqual(self.scenar.do.call_count, 1)

        self.assertEqual(self.mutex.acquire.call_count, 2)
        self.assertEqual(self.mutex.release.call_count, 2)

    @parameterized.expand(((MARKER.DECO, MARKER.ON), (MARKER.NONE, MARKER.ON), (MARKER.OFF, MARKER.ON), (MARKER.DECO, MARKER.OFF)))
    def test_do_secondary(self, marker, marker_init):
        with self.assertRaises(AssertionError):
            self.manager.do_scenar_secondary(Mock())
            return
        self.manager.initialize(self.scenar_init)
        self.scenar = Mock()
        self.scenar.get_marker.return_value = marker
        self.scenar_init.get_marker.return_value = marker_init
        self.manager.do_scenar_secondary(self.scenar)
        if marker == MARKER.NONE:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar_init)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar_init)
        else:
            self.assertEqual(self.manager.top(), self.scenar)
        if marker_init == MARKER.OFF or marker == MARKER.NONE:
            self.assertEqual(self.scenar.do.call_count, 1)
        self.assertEqual(self.mutex.acquire.call_count, 2)
        self.assertEqual(self.mutex.release.call_count, 2)


    def test_reload_current(self):
        self.manager.initialize(self.scenar_init)
        self.scenar = Mock()
        self.manager.reload_current_scenar(self.scenar)
        self.assertEqual(self.manager.get_current_scenar(), self.scenar)
        self.assertEqual(self.scenar.do.call_count, 0)

    def test_reload_selected(self):
        self.manager.initialize(self.scenar_init)
        self.scenar = Mock()
        self.manager.reload_scenar_selected(self.scenar)
        self.assertEqual(self.manager.get_scenar_select(), self.scenar)

    def test_reset(self):
        self.manager.initialize(self.scenar_init)
        self.scenar_stack = Mock()
        self.manager.push(self.scenar_stack)
        self.manager.push(self.scenar_stack)
        self.manager.reset()
        self.assertFalse(self.manager.get_stack())
        self.assertFalse(self.manager.get_current_scenar())
        self.assertFalse(self.manager.get_scenar_select())
        self.assertFalse(self.scenar_init.set_state.call_args[0][0])

    @parameterized.expand(((MARKER.DECO, MARKER.ON), (MARKER.NONE, MARKER.ON), (MARKER.DECO, MARKER.OFF)))
    def test_remove_second(self, marker, marker_init):
        self.manager.initialize(self.scenar_init)
        self.scenar_stack, self.scenar_stack2 = Mock(), Mock()
        self.manager.push(self.scenar_stack)
        self.manager.push(self.scenar_stack2)
        self.scenar_stack2.get_marker.return_value = marker
        self.scenar_init.get_marker.return_value = marker_init
        self.assertTrue(self.scenar_stack2 in self.manager.get_stack())
        self.manager.remove(self.scenar_stack2)
        if marker == MARKER.NONE:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar_init)
            self.assertEqual(self.manager.get_scenar_select(), self.scenar_init)
            self.assertEqual(self.scenar_stack2.do.call_count, 0)
        else:
            self.assertFalse(self.scenar_stack2 in self.manager.get_stack())
        self.assertEqual(self.mutex.acquire.call_count, 2)
        self.assertEqual(self.mutex.release.call_count, 2)
        self.manager.remove(Mock())

    @parameterized.expand(((MARKER.DECO, MARKER.ON), (MARKER.NONE, MARKER.ON), (MARKER.DECO, MARKER.OFF)))
    def test_remove_active(self, marker, marker_init):
        self.manager.initialize(self.scenar_init)
        self.scenar_stack, self.scenar_stack2 = Mock(), Mock()
        self.manager.push(self.scenar_stack)
        self.manager.push(self.scenar_stack2)
        self.scenar_stack.get_marker.return_value = marker
        self.scenar_init.get_marker.return_value = marker_init
        self.manager.reload_current_scenar(self.scenar_stack)
        if marker != MARKER.NONE:
            self.assertTrue(self.scenar_stack in self.manager.get_stack())
        self.manager.remove(self.scenar_stack)
        if marker == MARKER.NONE:
            self.assertEqual(self.manager.get_current_scenar(), self.scenar_stack)
            self.assertEqual(self.scenar_stack.do.call_count, 0)
        else:
            self.assertFalse(self.scenar_stack in self.manager.get_stack())
            if marker_init != MARKER.OFF:
                self.assertEqual(self.scenar_init.do.call_count, 2)
            else:
                self.assertEqual(self.scenar_stack2.do.call_count, 1)
        self.assertEqual(self.manager.get_scenar_select(), self.scenar_init)

        self.assertEqual(self.mutex.acquire.call_count, 2)
        self.assertEqual(self.mutex.release.call_count, 2)

    
    @parameterized.expand(((MARKER.DECO, ), (MARKER.NONE, ), (MARKER.ON,),  (MARKER.OFF,)))
    def test_get_state(self, marker):
        self.scenar_init.get_marker.return_value = marker
        self.manager.initialize(self.scenar_init)
        self.assertEqual(self.manager.get_state(), marker == MARKER.ON)
        self.assertEqual(self.manager.get_principal_state(), marker == MARKER.ON)
        self.assertEqual(self.manager.get_marker(), marker)

    def test_str(self):
        self.manager.initialize(self.scenar_init)
        self.scenar = Mock()
        self.manager.reload_current_scenar(self.scenar)
        self.scenar_stack = Mock()
        self.scenar_stack.name = "test"
        self.manager.push(self.scenar_stack)
        self.assertTrue(str(self.scenar_init.name) in str(self.manager))
        self.assertTrue(str(self.scenar.name) in str(self.manager))
        self.assertTrue(str(self.scenar_stack.name) in str(self.manager))
