import unittest
from tree.utils.Locker import Locker
from threading import Thread, Lock
from time import sleep
from unittest.mock import Mock, patch

class TestLocker(unittest.TestCase):
    def start(self, locker):
        locker.unlock()

    def test_lock(self):
        with patch("threading.Lock") as mock:
            locker = Locker()
            locker.lock()




