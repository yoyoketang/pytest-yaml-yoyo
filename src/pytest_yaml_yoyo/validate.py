"""
Built-in validate comparators.
"""
import re


def equals(check_value, expect_value):
    assert check_value == expect_value, f'{check_value} == {expect_value})'


def less_than(check_value, expect_value):
    assert check_value < expect_value, f'{check_value} < {expect_value})'


def less_than_or_equals(check_value, expect_value):
    assert check_value <= expect_value, f'{check_value} <= {expect_value})'


def greater_than(check_value, expect_value):
    assert check_value > expect_value, f'{check_value} > {expect_value})'


def greater_than_or_equals(check_value, expect_value):
    assert check_value >= expect_value, f'{check_value} >= {expect_value})'


def not_equals(check_value, expect_value):
    assert check_value != expect_value, f'{check_value} != {expect_value})'


def string_equals(check_value, expect_value):
    assert str(check_value) == str(expect_value), f'{check_value} == {expect_value})'


def length_equals(check_value, expect_value):
    expect_len = _cast_to_int(expect_value)
    assert len(check_value) == expect_len, f'{len(check_value)} == {expect_value})'


def length_greater_than(check_value, expect_value):
    expect_len = _cast_to_int(expect_value)
    assert len(check_value) > expect_len, f'{len(check_value)} > {expect_value})'


def length_greater_than_or_equals(check_value, expect_value):
    expect_len = _cast_to_int(expect_value)
    assert len(check_value) >= expect_len, f'{len(check_value)} >= {expect_value})'


def length_less_than(check_value, expect_value):
    expect_len = _cast_to_int(expect_value)
    assert len(check_value) < expect_len, f'{len(check_value)} < {expect_value})'


def length_less_than_or_equals(check_value, expect_value):
    expect_len = _cast_to_int(expect_value)
    assert len(check_value) <= expect_len, f'{len(check_value)} <= {expect_value})'


def contains(check_value, expect_value):
    assert isinstance(check_value, (list, tuple, dict, str))
    assert expect_value in check_value, f'{len(expect_value)} in {check_value})'


def contained_by(check_value, expect_value):
    assert isinstance(expect_value, (list, tuple, dict, str))
    assert check_value in expect_value, f'{len(check_value)} in {expect_value})'


def regex_match(check_value, expect_value):
    assert isinstance(expect_value, str)
    assert isinstance(check_value, str)
    assert re.match(expect_value, check_value)


def startswith(check_value, expect_value):
    assert str(check_value).startswith(str(expect_value)), f'{str(check_value)} startswith {str(expect_value)})'


def endswith(check_value, expect_value):
    assert str(check_value).endswith(str(expect_value)), f'{str(check_value)} endswith {str(expect_value)})'


def _cast_to_int(expect_value):
    try:
        return int(expect_value)
    except Exception:
        raise AssertionError(f"%{expect_value} can't cast to int")