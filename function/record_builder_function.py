from typing import Any


class RecordBuilderFunction:

    @staticmethod
    def apply(column_headers: list[str], result: tuple[Any,...]) -> dict[str, Any]:
        record: dict[str, Any] = {}

        for i in range(len(column_headers)):
            record[column_headers[i]] = result[i]

        return record
