import unittest
from unittest.mock import MagicMock
from client import update_logical_clock as update_logical_clock

class TestMethods(unittest.TestCase):
    def test_logical_clock_incremental(self):
        curr_clock_val = 100
        received_val = 0
        new_clock_val = update_logical_clock(curr_clock_val, received_val)
        self.assertEqual(new_clock_val, 101)

    def test_logical_clock_event(self):
        curr_clock_val = 100
        received_val = 200
        new_clock_val = update_logical_clock(curr_clock_val, received_val)
        self.assertEqual(new_clock_val, 201)

if __name__ == '__main__':
    unittest.main()