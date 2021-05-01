import unittest
from tree.utils.Locker import Locker
from threading import Thread
from unittest.mock import Mock, patch
import timeout_decorator
from time import sleep

class TestLocker(unittest.TestCase):
    def start(self, locker):
        while not locker.test():
            pass
        locker.unlock()

    @timeout_decorator.timeout(0.1)
    def test_lock(self):
        locker = Locker()
        Thread(target= lambda x=locker : self.start(x)).start()
        locker.lock()
        locker.lock()

    def test_locked(self):
        locker = Locker()
        self.assertFalse(locker.locked())
        locker.lock()
        self.assertTrue(locker.locked())
        proc = Thread(target=locker.lock)
        proc.start()
        proc.join(0.01)
        self.assertTrue(proc.is_alive())
        self.assertTrue(locker.test())
        locker.unlock()
        sleep(0.01)
        self.assertFalse(proc.is_alive())
        locker.unlock()
        self.assertFalse(locker.locked())





