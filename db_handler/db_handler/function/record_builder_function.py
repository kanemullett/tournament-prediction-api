from typing import Any


class RecordBuilderFunction:
    """
    Function for building records from database response objects.
    """

    @staticmethod
    def apply(column_headers: list[str], result: tuple[Any,...]) -> dict[str, Any]:
        """
        Convert database response objects into a record.

        Args:
            column_headers (list[str]): The headers of the response records.
            result (tuple[Any, ...]): The response record.

        Returns:
            dict[str, Any]: The built record.

        Examples:
            >>> RecordBuilderFunction.apply(["col1", "col2"], ("val1", "val2"))
            {
                "col1": "val1",
                "col2": "val2"
            }
        """
        record: dict[str, Any] = {}

        for i in range(len(column_headers)):
            record[column_headers[i]] = result[i]

        return record
