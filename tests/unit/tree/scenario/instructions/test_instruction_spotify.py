import unittest
from tree.scenario.instructions.Instruction_spotify import Instruction_spotify, TYPE_INST_SPOTIFY
from unittest.mock import Mock
from mock import patch
import threading
import pytest
from parameterized import parameterized

class TestInstructionSpotify(unittest.TestCase):
    def before(self, action):
        self.calculator, self.spotify, self.action, self.args = Mock(), Mock(), action, "args"
        self.duration, self.delay = "85", Mock()
        self.inst = Instruction_spotify(self.calculator, self.spotify, self.action, self.args, self.delay, False)

    
    @parameterized.expand(((TYPE_INST_SPOTIFY.next_track,), (TYPE_INST_SPOTIFY.start,),
                            (TYPE_INST_SPOTIFY.start_playlist,), (TYPE_INST_SPOTIFY.stop,), (TYPE_INST_SPOTIFY.volume,)))
    def test_run(self, action):
        self.before(action)
        self.count = 0
        def start(**kwargs):
            self.count += 1
            self.assertTrue(self.delay.wait.call_count)
            self.assertTrue(self.action in (TYPE_INST_SPOTIFY.start, TYPE_INST_SPOTIFY.start_playlist))
            if self.action == TYPE_INST_SPOTIFY.start_playlist:
                self.assertEqual(kwargs["context_uri"], self.args)

        def kill():
            self.count += 1
            self.assertEqual(self.action, TYPE_INST_SPOTIFY.stop)
            self.assertTrue(self.delay.wait.call_count)

        def set_volume(args):
            self.assertEqual(self.action, TYPE_INST_SPOTIFY.volume)
            self.count += 1
            self.assertTrue(self.delay.wait.call_count)

        def next_track():
            self.assertEqual(self.action, TYPE_INST_SPOTIFY.next_track)
            self.count += 1
            self.assertTrue(self.delay.wait.call_count)

        self.spotify.start.side_effect = start
        self.spotify.kill.side_effect = kill
        self.spotify.set_volume.side_effect = set_volume
        self.spotify.next_track.side_effect = next_track
        self.inst.run()
        self.assertEqual(self.count, 1)

    def test_str(self):
        self.before(TYPE_INST_SPOTIFY.start_playlist)
        self.assertTrue("spotify" in str(self.inst))
        self.assertTrue(str(self.action) in str(self.inst))
        self.assertTrue(str(self.args) in str(self.inst))
 
