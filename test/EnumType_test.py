import unittest

from spinward.core.EnumType import EnumType


class EnumTypeTest(unittest.TestCase):

    STRINGS = ["string", "alpha", "alphanum", "int", "float", "money"]
    STRINGS_COUNT = len(STRINGS)

    # Default: No base offset
    WgtTypes = EnumType(*STRINGS)
    print("WgtTypes items =", list(WgtTypes.items()))

    # Offset base
    OFFSET = 17
    WgtTypes2 = EnumType(base=OFFSET, *STRINGS)
    # print("WgtTypes2 items =", list(WgtTypes2.items()))
    # print("16 in WgtTypes2:", 16 in WgtTypes2)
    # 1/0


    def setUp(self):
        pass


    def test_items(self):
        expected = list(enumerate(self.STRINGS))
        actual = self.WgtTypes.items()
        self.assertEqual(actual, expected)


    def test_items_offset(self):
        expected = [(idx+self.OFFSET, name) for (idx, name) in enumerate(self.STRINGS)]
        actual = self.WgtTypes2.items()
        self.assertEqual(actual, expected)


    def test_getitem_numeric(self):
        expected = self.STRINGS
        actual = [self.WgtTypes[idx] for idx in range(self.STRINGS_COUNT)]
        self.assertEqual(actual, expected)


    def test_getitem_alpha_raise(self):
        with self.assertRaises(AttributeError):
            self.WgtTypes['bogus']


    def test_getitem_alpha_raise_offset(self):
        with self.assertRaises(AttributeError):
            self.WgtTypes2['bogus']


    def test_getitem_numeric_raise(self):
        with self.assertRaises(IndexError):
            self.WgtTypes[self.STRINGS_COUNT]


    def test_getitem_numeric_raise_offset(self):
        with self.assertRaises(IndexError):
            self.WgtTypes2[0]
        with self.assertRaises(IndexError):
            self.WgtTypes2[self.STRINGS_COUNT+self.OFFSET]


    def test_getitem_numeric_offset(self):
        expected = self.STRINGS
        actual = [self.WgtTypes2[idx] for idx in range(self.OFFSET, self.STRINGS_COUNT+self.OFFSET)]
        self.assertEqual(actual, expected)


    def test_getitem_string(self):
        expected = list(range(self.STRINGS_COUNT))
        actual = [self.WgtTypes[name] for name in self.STRINGS]
        self.assertEqual(actual, expected)


    def test_getitem_string_offset(self):
        expected = [idx + self.OFFSET for idx in range(self.STRINGS_COUNT)]
        actual = [self.WgtTypes2[name] for name in self.STRINGS]
        self.assertEqual(actual, expected)


    def test_contains_string_true(self):
        self.assertTrue("alpha" in self.WgtTypes)


    def test_contains_string_true_offset(self):
        self.assertTrue("alpha" in self.WgtTypes2)


    def test_contains_string_false(self):
        self.assertFalse("bogus" in self.WgtTypes)


    def test_contains_string_false_offset(self):
        self.assertFalse("bogus" in self.WgtTypes2)


    def test_contains_int_true(self):
        self.assertTrue(self.STRINGS_COUNT // 2 in self.WgtTypes)


    def test_contains_int_true_offset(self):
        self.assertTrue(self.STRINGS_COUNT // 2 + self.OFFSET in self.WgtTypes2)


    def test_contains_int_false(self):
        self.assertFalse(2 * self.STRINGS_COUNT in self.WgtTypes2)


    def test_contains_int_false_offset(self):
        self.assertFalse(0 in self.WgtTypes2)
        self.assertFalse(self.OFFSET - 1 in self.WgtTypes2)
        self.assertFalse(2 * self.STRINGS_COUNT in self.WgtTypes2)


if __name__ == '__main__':
    unittest.main()
