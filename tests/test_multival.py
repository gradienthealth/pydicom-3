# Copyright 2008-2018 pydicom3 authors. See LICENSE file for details.
"""Unit tests for the pydicom3.multival module."""

import pytest

from pydicom3 import config
from pydicom3.multival import MultiValue, ConstrainedList
from pydicom3.valuerep import DS, DSfloat, DSdecimal, IS, ISfloat
from copy import deepcopy

import sys

python_version = sys.version_info


class TestMultiValue:
    def testMultiDS(self):
        """MultiValue: Multi-valued data elements can be created"""
        multival = MultiValue(DS, ["11.1", "22.2", "33.3"])
        for val in multival:
            assert isinstance(val, DSfloat | DSdecimal)

    def testEmptyElements(self):
        """MultiValue: Empty number string elements are not converted"""
        multival = MultiValue(DSfloat, ["1.0", ""])
        assert 1.0 == multival[0]
        assert "" == multival[1]
        multival = MultiValue(IS, ["1", ""])
        assert 1 == multival[0]
        assert "" == multival[1]
        multival = MultiValue(DSdecimal, ["1", ""])
        assert 1 == multival[0]
        assert "" == multival[1]

        multival = MultiValue(IS, [])
        assert not multival
        assert 0 == len(multival)

    def testAppend(self):
        """MultiValue: Append of item converts it to required type"""
        multival = MultiValue(IS, [1, 5, 10])
        multival.append("5")
        assert isinstance(multival[-1], IS)
        assert 5 == multival[-1]

    def testSetIndex(self):
        """MultiValue: Setting list item converts it to required type"""
        multival = MultiValue(IS, [1, 5, 10])
        multival[1] = "7"
        assert isinstance(multival[1], IS)
        assert 7 == multival[1]

    def testDeleteIndex(self):
        """MultiValue: Deleting item at index behaves as expected"""
        multival = MultiValue(IS, [1, 5, 10])
        del multival[1]
        assert 2 == len(multival)
        assert 1 == multival[0]
        assert 10 == multival[1]

    def test_extend(self):
        """MultiValue: Extending a list converts all to required type"""
        multival = MultiValue(IS, [1, 5, 10])
        multival.extend(["7", 42])
        assert isinstance(multival[-2], IS)
        assert isinstance(multival[-1], IS)
        assert 7 == multival[-2]

        msg = "An iterable is required"
        with pytest.raises(TypeError, match=msg):
            multival.extend(None)

    def testSlice(self):
        """MultiValue: Setting slice converts items to required type."""
        multival = MultiValue(IS, range(7))
        multival[2:7:2] = [4, 16, 36]
        for val in multival:
            assert isinstance(val, IS)
        assert 16 == multival[4]

    def testIssue236DeepCopy(self):
        """MultiValue: deepcopy of MultiValue does not generate an error"""
        multival = MultiValue(IS, range(7))
        deepcopy(multival)
        multival = MultiValue(DS, range(7))
        deepcopy(multival)
        multival = MultiValue(DSfloat, range(7))
        deepcopy(multival)

    def testSorting(self):
        """MultiValue: allow inline sort."""
        multival = MultiValue(DS, [12, 33, 5, 7, 1])
        multival.sort()
        assert [1, 5, 7, 12, 33] == multival
        multival.sort(reverse=True)
        assert [33, 12, 7, 5, 1] == multival
        multival.sort(key=str)
        assert [1, 12, 33, 5, 7] == multival

    def test_equal(self):
        """MultiValue: test equality operator"""
        multival = MultiValue(DS, [12, 33, 5, 7, 1])
        multival2 = MultiValue(DS, [12, 33, 5, 7, 1])
        multival3 = MultiValue(DS, [33, 12, 5, 7, 1])
        assert multival == multival2
        assert not (multival == multival3)
        multival = MultiValue(str, ["a", "b", "c"])
        multival2 = MultiValue(str, ["a", "b", "c"])
        multival3 = MultiValue(str, ["b", "c", "a"])
        assert multival == multival2
        assert not (multival == multival3)

    def test_not_equal(self):
        """MultiValue: test equality operator"""
        multival = MultiValue(DS, [12, 33, 5, 7, 1])
        multival2 = MultiValue(DS, [12, 33, 5, 7, 1])
        multival3 = MultiValue(DS, [33, 12, 5, 7, 1])
        assert not multival != multival2
        assert multival != multival3
        multival = MultiValue(str, ["a", "b", "c"])
        multival2 = MultiValue(str, ["a", "b", "c"])
        multival3 = MultiValue(str, ["b", "c", "a"])
        assert not (multival != multival2)
        assert multival != multival3

    def test_str_rep(self):
        """MultiValue: test print output"""
        multival = MultiValue(IS, [])
        assert "" == str(multival)
        multival.extend(["1", 2, 3, 4])
        assert "[1, 2, 3, 4]" == str(multival)
        multival = MultiValue(str, [1, 2, 3])
        assert "['1', '2', '3']" == str(multival)
        multival = MultiValue(int, [1, 2, 3])
        assert "[1, 2, 3]" == str(multival)
        multival = MultiValue(float, [1.1, 2.2, 3.3])
        assert "[1.1, 2.2, 3.3]" == str(multival)
        mv = MultiValue(IS, [])
        mv._list = ["1234", b"\x01\x00"]
        assert "['1234', b'\\x01\\x00']" == str(mv)

    def test_setitem(self):
        """Test MultiValue.__setitem__()."""
        mv = MultiValue(int, [1, 2, 3])
        with pytest.raises(TypeError, match="'int' object is not iterable"):
            mv[1:1] = 4

        assert [1, 2, 3] == mv
        mv[1:1] = [4]
        assert [1, 4, 2, 3] == mv
        mv[1:2] = [5, 6]
        assert [1, 5, 6, 2, 3] == mv
        mv[1:3] = [7, 8]
        assert [1, 7, 8, 2, 3] == mv

    def test_iadd(self):
        """Test += [T, .]"""
        multival = MultiValue(IS, [1, 5, 10])
        multival += ["7", 42]
        assert isinstance(multival[-2], IS)
        assert isinstance(multival[-1], IS)
        assert 7 == multival[-2]

        msg = "An iterable is required"
        with pytest.raises(TypeError, match=msg):
            multival += None

    def test_IS_str(self):
        """Test IS works OK with empty str"""
        multival = MultiValue(ISfloat, [1, 2, "", 3, 4])
        assert multival == [1, 2, "", 3, 4]
        multival = MultiValue(IS, [1, 2, "", 3, 4])
        assert multival == [1, 2, "", 3, 4]

    def test_DS_str(self):
        """Test DS works OK with empty str"""
        multival = MultiValue(DSfloat, [1, 2, "", 3, 4])
        assert multival == [1, 2, "", 3, 4]
        multival = MultiValue(DSdecimal, [1, 2, "", 3, 4])
        assert multival == [1, 2, "", 3, 4]


def test_constrained_list_raises():
    """Test ConstrainedList raises if no _validate() override."""

    class Foo(ConstrainedList):
        pass

    msg = r"'Foo._validate\(\)' must be implemented"
    with pytest.raises(NotImplementedError, match=msg):
        Foo([1, 2, 3, 4])
