import unittest
from tree.utils.Dico import Dico

class TestDico(unittest.TestCase):
    def test_set_get(self):
        dico = Dico()
        dico.add("lol", 456145)
        self.assertEqual(dico.get("lol"), 456145)
        with self.assertRaises(AssertionError):
            dico.add(None, 45614)
        with self.assertRaises(KeyError):
            dico.get("k")

    def test_last(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*20)
        self.assertEqual(i*20, dico.last())

    def test_get_key(self):
        dico = Dico()
        dico.add("lol", 56)
        dico.add("xd", 56)
        self.assertEqual(dico.get_key(56), "lol")
        self.assertEqual(dico.get_key(50), None)

    def test_next(self):
        dico = Dico()
        for i in range(5,50):
            dico.add(i, i*2)
        self.assertEqual(dico.next(50), 52)
        with self.assertRaises(AssertionError):
            self.assertEqual(dico.next(111), 52)
        self.assertEqual(dico.next(98), 10)

    def test_iter(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*20)
        self.assertEqual(list(dico), [i*20 for i in range(0,50)]) 
        self.assertEqual(list(dico.keys()), [i for i in range(0,50)]) 

    def test_empty(self):
        dico = Dico()
        dico.add("lol", 42)
        self.assertFalse(dico.is_empty())
        dico.remove("lol")
        self.assertTrue(dico.is_empty())
        for i in range(0,50):
            dico.add(i, i*2)
        dico.clear()
        self.assertTrue(dico.is_empty())

    def test_zip(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*2)
        self.assertEqual(list(dico.zip()), list(zip(range(0,50), range(0,100,2))) )

    def test_str(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*2)
        self.assertEqual(str(dico), "\n".join(f"{i*2}" for i in range(0,50))+"\n")

    def test_eq(self):
        dico = Dico()
        dico2 = Dico()
        for i in range(0,50):
            dico.add(i, i*2)
            dico2.add(i, i*2)
        self.assertEqual(dico, dico2)
        dico2.remove(i)
        self.assertNotEqual(dico, dico2)
        self.assertNotEqual(dico, "")

    def test_get_index(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*2)
        self.assertEqual(dico.get_index(24), 24)
        self.assertEqual(dico.get_index(0), 0)

    def test_len(self):
        dico = Dico()
        for i in range(0,50):
            dico.add(i, i*2)

        self.assertEqual(len(dico), 50)






