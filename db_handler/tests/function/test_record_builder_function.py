from typing import Any

from db_handler.db_handler.function.record_builder_function import (
    RecordBuilderFunction
)
from predictor_common.test_resources.assertions import Assertions


class TestRecordBuilderFunction:

    __record_builder_function: RecordBuilderFunction = RecordBuilderFunction()

    def test_should_build_record_object_from_db_response(self):
        # Given
        headers: list[str] = ["id", "firstName", "lastName", "age"]
        response: tuple[Any, ...] = ("test-id", "Kane", "Mullett", 23)

        expected_record: dict[str, Any] = {
            "id": "test-id",
            "firstName": "Kane",
            "lastName": "Mullett",
            "age": 23
        }

        # When
        record: dict[str, Any] = (
            self.__record_builder_function.apply(headers, response)
        )

        # Then
        Assertions.assert_equals(expected_record, record)
