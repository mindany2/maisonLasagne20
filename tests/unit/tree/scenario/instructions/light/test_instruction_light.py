import unittest
from tree.scenario.instructions.light.Instruction_light import Instruction_light
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parameterized import parameterized

class TestInstructionLight(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.calculator, self.light, self.delay = Mock(), Mock(), Mock()
        self.duration = Mock()
        self.inst = Instruction_light(self.calculator, self.light, self.duration, self.delay, False)

    def test_eq(self):
        inst = Instruction_light(self.calculator, self.light, self.duration, self.delay, False)
        self.assertEqual(self.inst, inst)
        self.assertNotEqual(self.inst, 42)
        inst = Instruction_light(self.calculator, Mock(), self.duration, self.delay, False)
        self.assertNotEqual(self.inst, inst)

    def test_str(self):
        self.assertTrue(str(self.light.name) in str(self.inst))
        self.assertTrue("Light" in str(self.inst))

