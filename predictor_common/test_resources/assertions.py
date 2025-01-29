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