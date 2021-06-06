import unittest
from tree.connected_objects.dmx.Galaxy_laser import Galaxy_laser
from unittest.mock import Mock
from mock import patch
import timeout_decorator

@patch('time.sleep', return_value=None)
class TestGalaxyLaser(unittest.TestCase):
    def test_init(self, sleep):
        Galaxy_laser()
 
