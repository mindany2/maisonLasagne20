import unittest
import numpy as np
from tree.utils.Color import Color

class TestColor(unittest.TestCase):
    def test_init(self):
        color = Color(4566743)
        self.assertEqual("0x45AED7", str(color))
        color = Color("0x462481")
        self.assertEqual("0x462481", str(color))
        color = Color(0)
        self.assertEqual("0x000000", str(color))
        with self.assertRaises(TypeError):
            color = Color(None)

    def test_dim(self):
        color = Color("0x462481")
        color = color.dim(50)
        self.assertEqual("0x231240", str(color))

    def test_generate_array(self):
        color = Color(0)
        color2 = Color("0xffffff")
        array = color2.generate_array(color, 16*16-1)
        self.assertEqual(array, [f"0x{j}{i}{j}{i}{j}{i}" for j in "0123456789abcdef" for i in "0123456789abcdef"])

        color = Color("0x00ff00")
        color2 = Color("0xffffff")
        array = color2.generate_array(color, 16*16-1)
        self.assertEqual(array, [f"0x{j}{i}ff{j}{i}" for j in "0123456789abcdef" for i in "0123456789abcdef"])

    def test_hash(self):
        color = Color("0x462481")
        self.assertEqual("#462481", color.get_with_hash())

    def test_is_black(self):
        color = Color("0x462481")
        self.assertFalse(color.is_black())
        color = Color("0x000000")
        self.assertTrue(color.is_black())

    def test_set(self):
        color = Color("0x462481")
        color.set(Color("0xffffff"))
        self.assertEqual("0xFFFFFF", str(color))

    def test_eq(self):
        color = Color("0x462481")
        self.assertFalse(Color("0x14fe52") == color)
        self.assertTrue(Color(4596865) == color)
        

