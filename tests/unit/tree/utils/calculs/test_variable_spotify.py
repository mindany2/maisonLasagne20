import unittest
from tree.utils.calculs.Variable_spotify import Variable_spotify
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestVariable(unittest.TestCase):

    spotify = Mock()

    @pytest.fixture(autouse=True)
    def before(self):
        self.variable = Variable_spotify(self.spotify)
        self.assertEqual(self.variable.name, "spotify")

    @parametrize("val, result", [("lol", None), ("bpm", spotify.get_bpm()), ("volume", spotify.get_volume()), ("state", spotify.get_state())])
    def test_get(self, val, result):
        if not result:
            with self.assertRaises(NameError):
                self.variable.get(Mock(), val)
        else:
            self.assertEqual(self.variable.get(None, val), result)

    def test_set(self):
        with self.assertRaises(ReferenceError):
            self.variable.set(12)
 
    def test_reload(self):
        self.variable.reload(self.variable)
