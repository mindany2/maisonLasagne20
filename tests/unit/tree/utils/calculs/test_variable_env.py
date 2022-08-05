import unittest
from tree.utils.calculs.Variable_env import Variable_env
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize

class TestVariableEnv(unittest.TestCase):
    tree = Mock()
    env1 = Mock()
    var = Mock()
    
    @pytest.fixture(autouse=True)
    def before(self):
        self.inst = Mock()
        self.variable = Variable_env(self.tree)
        def get_env(name):
            if name == "env1.subenv1":
                return self.env1
            raise(KeyError)

        def get_var(name):
            if name == "var_name":
                return self.var
            raise(KeyError)
        self.tree.get_env.side_effect = get_env
        self.env1.get_var.side_effect = get_var
        self.assertEqual(self.variable.name, "env")

    @parametrize("name, validity, result", [["env", False, None], ["env.env1.subenv1.lol", False, None], ["env.env1.subenv1.var_name", True, var.get()],
        ["env.env1.subenv1", False, None], ["env.env1.subenv1.state", True, env1.state()], ["env.env1.subenv1.is_on", True, env1.is_on()]])
    def test_get(self, name, validity, result):
        if not validity:
            with self.assertRaises(KeyError):
                self.variable.get(self.inst, name)
            return
        self.assertEqual(self.variable.get(self.inst, name), result)

    def test_set(self):
        with self.assertRaises(ReferenceError):
            self.variable.set(12)

