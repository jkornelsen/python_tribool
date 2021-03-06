# -*- coding: utf-8 -*-

class Tribool(object):
    """Tribool implementation of three-valued logic.

    Tribool represents True, False, or Indeterminate using a private
    `_value` member set to True, False, or None respectively.
    """
    import threading as _threading
    _lock = _threading.Lock()
    _cache = {}

    def __new__(cls, value=None):
        """Create Tribool object.

        `value` may be any of True, False, None, Tribool or a name
        like 'True', 'False', 'None', 'Indeterminate', or 'Unknown'.
        None is representative of an indeterminate boolean value.
        Instances with the same value are identical (singleton-like).
        This method is thread-safe.
        """
        value = cls._resolve(value)

        if value not in cls._cache:
            with cls._lock:
                if value not in cls._cache:
                    result = super(Tribool, cls).__new__(cls)
                    result._value = value
                    cls._cache[value] = result

        return cls._cache[value]

    _names = {
        'True': True, 'False': False, 'None': None,
        'Indeterminate': None, 'Maybe': None, 'Unknown': None,
    }

    @classmethod
    def _resolve(cls, that):
        """Resolve given value to one of True, False, or None.

        Raises ValueError if given value's type is unsupported.
        """
        if that is True or that is False or that is None:
            return that
        elif isinstance(that, cls):
            return that._value
        elif that in cls._names:
            return cls._names[that]
        else:
            raise ValueError('Unsupported Value: ' + repr(that))

    @property
    def value(self):
        """Property representing the underlying value True, False or
        Indeterminate which are mapped to True, False or None in Python.
        """
        return self._value

    def __invert__(self):
        """Logical negation of Tribool value."""
        return Tribool(Tribool._not[self._value])

    def __and__(self, that):
        """Logical AND of Tribool and other value."""
        return Tribool(Tribool._and[self._value, self._resolve(that)])

    def __rand__(self, that):
        """Logical AND of Tribool and other value."""
        return Tribool(Tribool._and[self._value, self._resolve(that)])

    def __or__(self, that):
        """Logical OR of Tribool and other value."""
        return Tribool(Tribool._or[self._value, self._resolve(that)])

    def __ror__(self, that):
        """Logical OR of Tribool and other value."""
        return Tribool(Tribool._or[self._value, self._resolve(that)])

    def __xor__(self, that):
        """Logical XOR of Tribool and other value."""
        return Tribool(Tribool._xor[self._value, self._resolve(that)])

    def __rxor__(self, that):
        """Logical XOR of Tribool and other value."""
        return Tribool(Tribool._xor[self._value, self._resolve(that)])

    def __eq__(self, that):
        """Logical equality of Tribool and other value."""
        return Tribool(Tribool._eq[self._value, self._resolve(that)])

    def __ne__(self, that):
        """Logical inequality of Tribool and other value."""
        return ~Tribool(Tribool._eq[self._value, self._resolve(that)])

    def __lt__(self, that):
        """Logical less than of Tribool and other value."""
        return Tribool(Tribool._lt[self._value, self._resolve(that)])

    def __le__(self, that):
        """Logical less than or equal of Tribool and other value."""
        return (Tribool(Tribool._lt[self._value, self._resolve(that)])
                | (self == that))

    def __gt__(self, that):
        """Logical greater than of Tribool and other value."""
        return ~(self <= that)

    def __ge__(self, that):
        """Logical greater than or equal of Tribool and other value."""
        return ~(self < that)

    def __hash__(self):
        """Hash of Tribool."""
        return id(self)

    def __nonzero__(self):
        """Raise ValueError on conversion to bool.

        When this occurs, it may indicate that the logical operators:
        (and, or, not) were used. Python does not permit overloading these
        operators. Use the bitwise (&, |, ^, ~) operators instead.
        Likewise, if the comparison operators (<, <=, >, >=) were used
        then a type conversion using Tribool(...) is required.
        """
        raise ValueError('Cannot implicitly convert Tribool to bool'
                         ' (use the bitwise (&, |, ^, ~) operators'
                         ' or insert a cast and use Tribool(...).value)')

    __bool__ = __nonzero__

    def __index__(self):
        """Raise ValueError on conversion to int."""
        raise ValueError('Cannot convert Tribool to index')

    def __trunc__(self):
        """Raise ValueError on truncation."""
        raise ValueError('Connect truncate Tribool')

    def __str__(self):
        """String representing Tribool value."""
        return 'Indeterminate' if self._value is None else str(self._value)

    def __repr__(self):
        """String representation of Tribool."""
        return 'Tribool({0})'.format(str(self._value))

    def __copy__(self):
        """Value of copy.copy()."""
        return self

    def __deepcopy__(self, memo):
        """Value of copy.deepcopy()."""
        return self

    def _check(self):
        """Check invariant of Tribool."""
        assert (self._value in (True, False, None))
        return self

    """Logic tables for operators."""

    _not = { True : False,
             False : True,
             None : None }

    _and = { (True, True) : True,
             (True, False) : False,
             (True, None) : None,
             (False, True) : False,
             (False, False) : False,
             (False, None) : False,
             (None, True) : None,
             (None, False) : False,
             (None, None) : None }

    _or = { (True, True) : True,
            (True, False) : True,
            (True, None) : True,
            (False, True) : True,
            (False, False) : False,
            (False, None) : None,
            (None, True) : True,
            (None, False) : None,
            (None, None) : None }

    _xor = { (True, True) : False,
             (True, False) : True,
             (True, None) : None,
             (False, True) : True,
             (False, False) : False,
             (False, None) : None,
             (None, True) : None,
             (None, False) : None,
             (None, None) : None }

    _eq = { (True, True) : True,
            (True, False) : False,
            (True, None) : None,
            (False, True) : False,
            (False, False) : True,
            (False, None) : None,
            (None, True) : None,
            (None, False) : None,
            (None, None) : None }

    _lt = { (True, True) : False,
            (True, False) : False,
            (True, None) : False,
            (False, True) : True,
            (False, False) : False,
            (False, None) : None,
            (None, True) : None,
            (None, False) : False,
            (None, None) : None }

__title__ = 'tribool'
__version__ = '0.5.4'
__build__ = 0x000504
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Grant Jenks'
