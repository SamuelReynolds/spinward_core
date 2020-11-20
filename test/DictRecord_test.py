import unittest
from copy import deepcopy
from parameterized import parameterized

from spinward.core.DictRecord import DictRecord


class dict_util_Test(unittest.TestCase):

    def setUp(self):
        pass


    def test_update_recursive_0(self):
        dict0 = dict(a=1, b=2, c=3)
        dict1 = dict(
            b = dict(f=1, g=2),
            d = 4
        )
        expected = DictRecord(dict0)
        expected['b'] = dict1['b']
        expected['d'] = dict1['d']
        expected.normalize()
        dict0 = DictRecord.from_dict(dict0)
        dict0.update_recursive(dict1)
        # dict0.dump()
        self.assertEqual(dict0, expected)


    def test_update_recursive_1(self):
        dict0 = dict(
            a   = 1,
            b   = dict(f=1, g=2),
            c   = 3
        )
        dict1 = dict(
            b=dict(g=5, h=3),
            d=4
        )
        expected = DictRecord(dict0)
        expected['b'].update(dict1['b'])
        expected['d'] = dict1['d']
        dict0 = DictRecord.from_dict(dict0)
        dict0.update_recursive(dict1)
        # dict0.dump()
        self.assertEqual(dict0, expected)


    def test_as_dict(self):
        dr0 = DictRecord(
            a=1,
            b=DictRecord(f=1, g=2, h=3),
            c=3
        )
        expected = dict(
            a=1,
            b=dict(f=1, g=2, h=3),
            c=3
        )
        actual = dr0.as_dict()
        self.assertEqual(actual, expected)
        self.assertTrue(isinstance(actual['b'], dict))


    _dict0 = dict(
        a=1,
        b=dict(f=1, g=2),
        c=3
    )
    _dr0x0 = DictRecord.from_dict(_dict0)
    _dr0x0.b.x = deepcopy(_dict0)
    _dr0x0.normalize()

    _NOTHING = object()

    @parameterized.expand([  # source, keys, default, expected
        (_dr0x0, 'b.g', None, 2,),
        (_dr0x0, 'b.x', None, _dict0),
        (_dr0x0, 'b.z', None, None),
        (_dr0x0, 'b.z', _NOTHING, None),
    ])
    def test_get_nested(self, drec, keys, default, expected, delim='.'):
        if isinstance(keys, str):
            keys = keys.split(delim)
        if default is self._NOTHING:
            actual = drec.get_nested(keys)
        else:
            actual = drec.get_nested(keys, default)
        self.assertEqual(actual, expected)


    _dict1x0 = deepcopy(_dict0)
    _dict1x1 = deepcopy(_dict0); _dict1x1['b']['g'] = 5
    _dict1x2 = deepcopy(_dict0); _dict1x2['b']['x'] = 7
    _dict1x3 = deepcopy(_dict0); _dict1x3['b']['g'] = deepcopy(_dict0)
    _dict1x4 = {'b':{}}


    @parameterized.expand([  # source, keys, value, expected, extend
        (_dict1x0, 'b.g', 5, _dict1x1, False,),
        (_dict1x0, 'b.x', 7, _dict1x2, False),
        (_dict1x0, 'b.g', _dict0, _dict1x3, False),
        (_dict1x4, 'b.x', 17, {'b': {'x': 17}}, False),
        (_dict1x4, 'b.g.x', 17, {'b': {'g': {'x': 17}}}, True),
        (_dict1x4, 'b.g.x.z', 17, {'b': {'g': {'x': {'z': 17}}}}, True),
    ])
    def test_dict_set_nested(self, dct0, keys, val, expected, extend=False, delim='.'):
        if isinstance(keys, str):
            keys = keys.split(delim)
        actual = DictRecord.from_dict(dct0)
        actual.set_nested(keys, val, extend=extend)
        self.assertEqual(actual, expected)


    @parameterized.expand([
        (False,),
        (True,)
    ])
    def test_dict_set_nested_keyerror_noraise(self, extend):
        keys = 'b.g.x.z'.split('.')
        actual = DictRecord.from_dict(self._dict1x4)
        actual.b.g = 13
        with self.assertRaises(KeyError):
            actual.set_nested(keys, 1234, extend=extend)


if __name__ == '__main__':
    unittest.main()
