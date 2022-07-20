import unittest
from tree.scenario.Scenario import Scenario, MARKER, Instructions_list
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestScenario(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator = Mock()
        self.name, self.marker = "name test", Mock()
        self.scenario = Scenario(self.name, self.marker, self.calculator)

    @patch.object(Instructions_list, "add")
    def test_add(self, list_inst):
        inst = Mock()
        self.scenario.add_inst(inst)
        self.assertEqual(list_inst.call_count, 1)
        self.assertEqual(list_inst.call_args[0][0], inst)

    def test_get_marker(self):
        self.assertEqual(self.scenario.get_marker(), self.marker)

    @patch.object(Instructions_list, "get_state")
    @patch.object(Instructions_list, "set_state")
    def test_state(self, set_state, get_state):
        get_state.return_value = False
        self.assertEqual(self.scenario.state(), False)
        self.scenario.set_state(True)
        self.assertEqual(set_state.call_count, 1)
        self.assertEqual(set_state.call_args[0][0], True)
        get_state.return_value = True
        self.assertEqual(self.scenario.state(), True)

    @patch.object(Instructions_list, "get_state")
    @patch.object(Instructions_list, "set_state")
    def test_reload(self, set_state, get_state):
        self.scenario.set_state(True)
        self.scenario2 = Scenario(self.name, self.marker, self.calculator)
        self.scenario2.reload(self.scenario)
        self.assertTrue(self.scenario2.state())


    @parameterized.expand(((MARKER.OFF,), (MARKER.NONE,)))
    @patch.object(Instructions_list, "do")
    def test_do(self, marker, do):
        self.cond = threading.Condition()
        def list_do(finish):
            self.assertEqual(finish, marker == MARKER.NONE)
            self.assertTrue(str(self.name) in str(threading.current_thread()))
            with self.cond:
                self.cond.wait()
        self.scenario.marker = marker
        do.side_effect = list_do
        self.scenario.do()
        self.assertEqual(threading.active_count(), 2)
        with self.cond:
            self.cond.notify_all()
        self.assertEqual(do.call_count, 1)
 
    @parameterized.expand(((MARKER.OFF,), (MARKER.NONE,)))
    @patch.object(Instructions_list, "do")
    def test_do_join(self, marker, do):
        self.cond = threading.Condition()
        def list_do(finish):
            self.assertEqual(finish, marker == MARKER.NONE)
            self.assertTrue(str(self.name) in str(threading.current_thread()))
            with self.cond:
                self.cond.wait(0.001)
        self.scenario.marker = marker
        do.side_effect = list_do
        self.scenario.do(join=True)
        self.assertEqual(threading.active_count(), 1)
       
    #TODO
    """
    def test_eq(self):
        self.scenario2 = Scenario(self.name, self.marker, self.calculator)
        self.assertEqual(self.scenario, self.scenario2)
    """

    @patch.object(Instructions_list, "initialize")
    def test_initialize(self, initialize):
        self.scenario.initialize()
        self.assertEqual(initialize.call_count, 1)

    @patch.object(Instructions_list, "__str__")
    def test_str(self, string):
        string.return_value = str(Mock())
        self.assertTrue(str(self.name) in str(self.scenario))
        self.assertTrue(str(self.marker) in str(self.scenario))
        self.assertTrue(str(string.return_value) in str(self.scenario))
        self.assertTrue("state" in str(self.scenario))



        


