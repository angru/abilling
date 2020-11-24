from tests.utils import EqMock


def test_eqmock():
    some_value = EqMock()

    assert some_value == 1
    assert some_value == 0.5
    assert some_value == 'hello'

    only_int = EqMock(int)

    assert only_int != 'hello'
    assert only_int != 0.5
    assert only_int == 1
    assert only_int == 2

    only_first = EqMock(remember=True)

    assert only_first == 1
    assert only_first != 2
    assert only_first != 'hello'
    assert only_first == 1

    only_first_and_str = EqMock(str, remember=True)

    assert only_first_and_str != 1
    assert only_first_and_str == 'hello'
    assert only_first_and_str != 'world'

    int_or_str = EqMock((int, str))

    assert int_or_str == 1
    assert int_or_str == 'hello'
    assert int_or_str != 0.5
