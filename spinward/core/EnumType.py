#   EnumType.py
"""
Enumerated-values class.
"""


class EnumType(object):
    """
    Enumerated-values class.

    Allows reference to enumerated values by name
    or by index (i.e., bidirectional mapping).

    E.g.,
        |	Status = EnumType('A', 'B', 'C')
        |	mya = MyEnums.A
        |	myb = MyEnums.B
        |
        |	for idx,name in MyEnums:
        |		print(idx, name)
        |
        |	mybString = MyEnums[myb]

    """

    def __init__(self, *names, **kwargs):
        # Remember names list for reference by index
        self._names = list(names)
        self._base = kwargs.get('base', 0)
        # Attributes for direct reference
        for _i, _s in enumerate(self._names):
            setattr(self, _s, _i + self._base)


    def __contains__(self, key):
        if isinstance(key, int):
            return key >= self._base and key - self._base < len(self._names)
        return key in self._names


    def __iter__(self):
        it = iter(self._names)  # pylint: disable=invalid-name
        idx = 0
        while 1:
            yield (idx + self._base, it.next())
            idx += 1


    def __getitem__(self, key):         # pylint: disable=missing-function-docstring
        if isinstance(key, int):
            return self._names[key - self._base]
        return self._name_to_enum(key)


    def __setitem__(self, key, value):  # pylint: disable=missing-function-docstring
        raise KeyError('Attempted to change enumeration value')


    def __len__(self):                  # pylint: disable=missing-function-docstring
        return len(self._names)


    def items(self):
        """
        @return ordered list of enumerated (value, name) tuples
        """
        return [(idx + self._base, self._names[idx])
                for idx in range(0, len(self._names))]

    def names(self):
        """
        @return ordered list of enumerated value _names
        """
        return self._names[:]


    def values(self):
        """
        @return ordered list of enumerated values
        """
        return [self._name_to_enum(name) for name in self._names]


    def _name_to_enum(self, name):
        """
        @return enumeration value corresponding to names
        """
        try:
            return getattr(self, name)
        except ValueError as exc:
            args = list(exc.args)
            args.append("Unknown enum value name '%s'" % name)
            args = tuple(args)
            exc.args = args
            raise
