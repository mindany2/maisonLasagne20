import unittest
from tree.scenario.Instructions_list import Instructions_list
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestIntructionList(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator = Mock()
        self.list_insts = Instructions_list(False, self.calculator)
        self.inst1, self.inst2, self.inst3 = Mock(), Mock(), Mock()
        self.inst1.synchro = False
        self.inst2.synchro = True
        self.inst3.synchro = False
        self.insts = [self.inst1, self.inst2, self.inst3]
        for inst in self.insts:
            self.list_insts.add(inst)

    def test_add(self):
        self.assertEqual(self.list_insts.list, self.insts)
        self.assertEqual(self.list_insts.list_barrier, [1, 2, 0])

    def test_set_state(self):
        self.assertFalse(self.list_insts.state)
        self.list_insts.set_state(True)
        self.assertTrue(self.list_insts.state)
        self.list_insts.set_state(False)
        self.assertFalse(self.list_insts.state)
        for inst in self.insts:
            self.assertEqual(inst.finish.call_count, 1)

    def test_finish(self):
        self.cond = threading.Condition()

        def wait():
            with self.cond:
                self.cond.wait()

        self.inst1.finish.side_effect = wait
        self.inst2.finish.side_effect = wait
        self.inst3.finish.side_effect = wait

        self.list_insts.finish()
        self.assertEqual(threading.active_count(), 4)
        with self.cond:
            self.cond.notify_all()
        for inst in self.insts:
            self.assertEqual(inst.finish.call_count, 1)

    def test_iter(self):
        for inst1, inst2 in zip(self.list_insts, self.insts):
            self.assertEqual(inst1, inst2)


    @parameterized.expand(((False,), (True,)))
    def test_do(self, finish):
        self.count = 0
        self.cond = threading.Condition()
        self.mutex = threading.Lock()
        def run(barrier):
            self.mutex.acquire()
            sleep(0.001)
            self.assertEqual(barrier.parties, [1,2,2][self.count])
            self.assertTrue(str(self.insts[self.count]) in threading.current_thread().getName())
            self.count += 1
            self.assertEqual(threading.active_count(), 3*(self.count<3)+ 2*(self.count==3))
            self.mutex.release()
            with self.cond:
                if self.count > 1:
                    self.cond.wait(0.001)
                    self.cond.notify_all()
                else:
                    self.cond.wait()

        self.inst1.run.side_effect = run
        self.inst2.run.side_effect = run
        self.inst3.run.side_effect = run
        self.inst1.wait_precedent.return_value = False
        self.inst2.wait_precedent.return_value = False
        self.inst3.wait_precedent.return_value = True

        self.list_insts.do(finish)
        self.assertEqual(threading.active_count(), 1)
        if finish:
            for inst in self.insts:
                self.assertEqual(inst.finish.call_count, 1)

    def test_loop(self):
        self.count = 0
        self.mutex = threading.Lock()
        def run(barrier):
            self.mutex.acquire()
            self.count += 1
            if self.count > 40:
                self.list_insts.loop = False
            self.mutex.release()

        self.inst1.run.side_effect = run
        self.inst2.run.side_effect = run
        self.inst3.run.side_effect = run
        self.inst1.wait_precedent.return_value = False
        self.inst2.wait_precedent.return_value = False
        self.inst3.wait_precedent.return_value = False
        self.list_insts.loop = True
        self.list_insts.state = True
        self.list_insts.do()
        self.assertEqual(threading.active_count(), 1)
        self.assertEqual(self.count, 42)

    def test_initialize(self):
        self.list_insts.initialize()
        for inst in self.insts:
            self.assertEqual(inst.initialize.call_count, 1)

    def test_str(self):
        self.list_insts.loop = True
        self.assertTrue("Loop" in str(self.list_insts))
        for inst in self.insts:
            self.assertTrue(str(inst) in str(self.list_insts))

        


 
