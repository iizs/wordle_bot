import unittest
from wordle.util import mark


class TestMark(unittest.TestCase):

    def test_mark_001(self):
        self.assertEqual(mark('every', 'redye'), '🟨🟨⬛🟨🟨')
