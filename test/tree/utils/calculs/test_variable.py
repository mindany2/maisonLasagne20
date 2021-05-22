import unittest
from tree.utils.calculs.Variable import Variable
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestVariable(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.name, self.val = "test", 42
        self.action_set, self.action_get = Mock(), Mock()
        self.inst1, self.inst2 = Mock(), Mock()
        self.variable = Variable(self.name, self.val, self.action_get, self.action_set)

    @parametrize("inst", [None, Mock()])
    @parametrize("val", [None, 12])
    def test_get(self, inst, val):
        self.action_get.return_value = val
        if val:
            self.assertEqual(self.variable.get(inst=inst), val)
        else:
            self.assertEqual(self.variable.get(inst=inst), self.val)
        self.assertEqual(self.action_get.call_count, 1)
        if inst:
            self.assertTrue(inst in self.variable.list_inst)

    def test_reset(self):
        self.variable.add_inst(self.inst1)
        self.variable.add_inst(self.inst2)
        for inst1, (id_, inst) in zip([self.inst1, self.inst2], self.variable.list_inst.zip()):
            self.assertEqual(id_, inst1.get_id())
            self.assertEqual(inst, inst1)
        self.variable.reset()
        self.assertTrue(self.variable.list_inst.is_empty())

    def test_reload(self):
        self.variable2 = Variable(self.name,  0)
        self.variable2.reload(self.variable)
        self.assertEqual(self.variable.get(), self.variable2.get())

    def test_set(self):
        self.action_get.return_value = None
        self.inst1.current = False
        self.inst2.current = True
        self.cond = threading.Condition()
        self.count = 0
        def wait_action(val):
            self.count += 1
            self.assertEqual(val, self.value)
            self.assertTrue(str(self.name) in str(threading.current_thread()))
            with self.cond:
                self.cond.wait()

        def wait_inst(duration):
            self.count += 1
            self.assertEqual(duration, self.duration)
            self.assertTrue(str(self.name) in str(threading.current_thread()))
            self.assertTrue(str(self.inst2) in str(threading.current_thread()))
            with self.cond:
                self.cond.wait()

        self.variable.add_inst(self.inst1)
        self.variable.add_inst(self.inst2)
        self.value = 89
        self.duration = 7
        self.action_set.side_effect = wait_action
        self.inst1.reload.side_effect = wait_inst
        self.inst2.reload.side_effect = wait_inst
        self.variable.set(self.value, self.duration)
        
        with self.cond:
            self.cond.notify_all()

        self.assertEqual(self.count, 2)
        self.assertEqual(self.variable.get(), self.value)

        self.assertEqual(threading.active_count(), 3)
 

    def test_int(self):
        self.assertEqual(int(self.variable), self.val)

    def test_str(self):
        self.variable.add_inst(self.inst1)
        self.variable.add_inst(self.inst2)
        self.assertTrue(str(self.name) in str(self.variable))
        self.assertTrue(str(self.val) in str(self.variable))
        self.assertTrue(str(self.inst1) in str(self.variable))
        self.assertTrue(str(self.inst2) in str(self.variable))
