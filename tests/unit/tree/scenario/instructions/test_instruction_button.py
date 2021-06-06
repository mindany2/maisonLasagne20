import unittest
from tree.scenario.instructions.Instruction_button import Instruction_button, TYPE_BUTTON, Button_principal, Button_secondary, Instruction
from unittest.mock import Mock
from mock import patch
import threading
from time import sleep
import pytest


class TestInstructionButton(unittest.TestCase):

    def before(self, type_bt, nb_scenar=None):
        if not nb_scenar:
            nb_scenar = 1 + int(type_bt == TYPE_BUTTON.principal)
        self.calculator, self.delay = Mock(), Mock()
        self.calculator.eval.return_value = 42
        self.reader, self.condition = Mock(), Mock()
        self.scenar1, self.scenar2 = Mock(), Mock()
        self.env, self.preset = Mock(), Mock()
        list_scenar = [self.scenar1] + [self.scenar2]*(nb_scenar==2)
        self.reader.get_scenarios.return_value = [self.env, self.preset, list_scenar]
        self.inst = Instruction_button(self.calculator, self.reader, type_bt, self.delay, self.condition, False)

    @patch.object(Button_principal, "__init__", return_value=None)
    def test_initialize_principal(self, init_bt):
        self.before(TYPE_BUTTON.principal)
        with self.assertRaises(AssertionError):
            self.inst.run()
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 3)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.condition)
        self.assertEqual(self.reader.get_scenarios.call_count, 1)
        self.assertEqual(init_bt.call_count, 1)
        self.assertEqual(init_bt.call_args[0][0], f"{self.env.name}.{self.preset.name}.{self.scenar1.name}")
        self.assertEqual(init_bt.call_args[0][1], self.preset.get_manager())
        self.assertEqual(init_bt.call_args[0][2], self.scenar1)
        self.assertEqual(init_bt.call_args[0][3], self.scenar2)
        

    @patch.object(Button_secondary, "__init__", return_value=None)
    def test_initialize_secondary(self, init_bt):
        self.before(TYPE_BUTTON.secondary)
        self.inst.initialize()
        self.assertEqual(self.calculator.eval.call_count, 2)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.condition)
        self.assertEqual(self.reader.get_scenarios.call_count, 1)
        self.assertEqual(init_bt.call_count, 1)
        self.assertEqual(init_bt.call_args[0][0], f"{self.env.name}.{self.preset.name}.{self.scenar1.name}")
        self.assertEqual(init_bt.call_args[0][1], self.preset.get_manager())
        self.assertEqual(init_bt.call_args[0][2], self.scenar1)

    def test_initialize_fail(self):
        self.before(None)
        self.inst.initialize()
        self.assertEqual(self.condition.raise_error.call_count, 1)

    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_run_principal(self, init_bt, press):
        self.before(TYPE_BUTTON.principal)
        self.env.get_preset_select.return_value = self.preset
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(self.calculator.eval.call_count, 4)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.condition)
        self.assertEqual(press.call_count, 1)
        self.assertEqual(press.call_args.kwargs["state"],self.calculator.eval())
 
    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_run_principal_1_scenar(self, init_bt, press):
        self.before(TYPE_BUTTON.principal, nb_scenar=1)
        self.env.get_preset_select.return_value = self.preset
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(self.calculator.eval.call_count, 4)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.condition)
        self.assertEqual(press.call_count, 1)
        with self.assertRaises(KeyError):
            self.assertEqual(press.call_args.kwargs["state"],self.calculator.eval())
 
    @patch.object(Button_secondary, "press")
    @patch.object(Button_secondary, "__init__", return_value=None)
    def test_run_secondary(self, init_bt, press):
        self.before(TYPE_BUTTON.secondary)
        self.env.get_preset_select.return_value = self.preset
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(self.calculator.eval.call_count, 4)
        self.assertEqual(self.calculator.eval.call_args[0][0], self.condition)
        self.assertEqual(press.call_count, 1)

    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_run_not_actual_preset(self, init_bt, press):
        self.before(TYPE_BUTTON.principal)
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(press.call_count, 0)
 
    @patch.object(Instruction, "run")
    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_run_not_current(self, init_bt, press, run):
        def side_effect():
            self.inst.current = False
        run.side_effect = side_effect
        self.before(TYPE_BUTTON.principal)
        self.env.get_preset_select.return_value = self.preset
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(press.call_count, 0)
  
    @patch.object(Instruction, "run")
    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_run_current(self, init_bt, press, run):
        def side_effect():
            self.inst.current = True
        run.side_effect = side_effect
        self.before(TYPE_BUTTON.principal)
        self.env.get_preset_select.return_value = self.preset
        self.inst.initialize()
        self.inst.run()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(press.call_count, 1)

    @patch.object(Button_principal, "press")
    @patch.object(Button_principal, "__init__", return_value=None)
    def test_finish_principal(self, init_bt, press):
        self.before(TYPE_BUTTON.principal)
        self.inst.initialize()
        self.inst.finish()
        self.assertEqual(press.call_count, 0)
 
    @patch.object(Button_secondary, "press")
    @patch.object(Button_secondary, "__init__", return_value=None)
    def test_finish_secondary(self, init_bt, press):
        self.before(TYPE_BUTTON.secondary)
        self.inst.initialize()
        self.inst.finish()
        self.assertEqual(press.call_count, 1)
        self.assertEqual(press.call_args.kwargs["state"],False)

    def test_eq(self):
        self.before(TYPE_BUTTON.secondary)
        self.inst.initialize()
        inst2 = Instruction_button(self.calculator, self.reader, TYPE_BUTTON.secondary, self.delay, self.condition, False)
        inst2.initialize()
        self.assertEqual(self.inst, inst2)
        self.assertNotEqual(self.inst, 42)
        inst2 = Instruction_button(self.calculator, self.reader, TYPE_BUTTON.secondary, self.delay, "other_condition", False)
        self.assertNotEqual(self.inst, inst2)
        inst2 = Instruction_button(self.calculator, self.reader, TYPE_BUTTON.principal, self.delay, self.condition, False)
        self.assertNotEqual(self.inst, inst2)
        inst2 = Instruction_button(self.calculator, self.reader, TYPE_BUTTON.secondary, Mock(), self.condition, False)
        self.assertNotEqual(self.inst, inst2)
        inst2 = Instruction_button(self.calculator, Mock(), TYPE_BUTTON.secondary, self.delay, self.condition, False)
        self.assertNotEqual(self.inst, inst2)

    def test_str(self):
        self.before(TYPE_BUTTON.secondary)
        self.inst.initialize()
        self.assertTrue("Bouton" in str(self.inst))
        self.assertTrue(str(TYPE_BUTTON.secondary) in str(self.inst))
        self.assertTrue(str(self.reader) in str(self.inst))
 

 







