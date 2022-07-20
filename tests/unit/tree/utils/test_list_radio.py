import unittest
from tree.utils.List_radio import List_radio
from unittest.mock import Mock

class TestListRadio(unittest.TestCase):
    def test_init(self):
        list_test = List_radio()
        self.assertEqual(list_test.selected(), None)

    def test_add(self):
        list_test = List_radio()
        mocks = []
        for i in range(0,20):
            element = Mock()
            element.name = i
            list_test.add(element)
            mocks.append(element)
        self.assertEqual(mocks[0].change_state.call_count, 1)
        self.assertEqual(mocks[0].change_state.call_args[0][0], True)
        self.assertEqual(list_test.selected(), mocks[0])

        list_test = List_radio()
        element = Mock()
        list_test.add(element, change=False)
        self.assertEqual(element.change_state.call_count, 0)
        self.assertEqual(list_test.selected(), element)

    def test_change(self):
        list_test = List_radio()
        mocks = []
        for i in range(0,20):
            element = Mock()
            element.name = i
            list_test.add(element)
            mocks.append(element)
        list_test.change_select(mocks[12])
        self.assertEqual(mocks[12].change_state.call_count, 1)
        self.assertEqual(mocks[0].change_state.call_args[0][0], False)
        self.assertEqual(mocks[12].change_state.call_args[0][0], True)
        self.assertEqual(list_test.selected(), mocks[12])

    def test_next(self):
        list_test = List_radio()
        mocks = []
        for i in range(0,20):
            element = Mock()
            element.name = i
            list_test.add(element)
            mocks.append(element)
        list_test.change_select(mocks[12])
        list_test.next()
        self.assertEqual(mocks[13].change_state.call_count, 1)
        self.assertEqual(mocks[13].change_state.call_args[0][0], True)
        self.assertEqual(list_test.selected(), mocks[13])

