from typing import Any


class Assertions:

    @staticmethod
    def assert_equals(expected: Any, actual: Any) -> None:
        assert expected == actual

    @staticmethod
    def assert_true(condition: bool) -> None:
        assert condition

    @staticmethod
    def assert_false(condition: bool) -> None:
        assert condition is False

    @staticmethod
    def assert_none(actual: Any) -> None:
        assert actual is None

    @staticmethod
    def assert_type(expected_type: type, actual: Any) -> None:
        assert isinstance(actual, expected_type)
