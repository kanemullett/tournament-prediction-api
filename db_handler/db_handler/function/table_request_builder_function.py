from db_handler.db_handler.model.column_definition import ColumnDefinition
from db_handler.db_handler.model.table_definition import TableDefinition


class TableRequestBuilderFunction:
    """
    Function for building SQL table creation requests from TableDefinition
    objects.
    """

    def apply(self, table_definition: TableDefinition) -> str:
        """
        Convert a TableDefinition object into a SQL table creation request.

        Args:
            table_definition (TableDefinition): The TableDefinition object to
                be converted.

        Returns:
            str: The SQL table creation request.
        """
        string_parts: list[str] = [
            "CREATE TABLE IF NOT EXISTS",
            self.__build_table(
                table_definition.schema_,
                table_definition.table
            ),
            self.__build_columns(
                table_definition.columns
            ),
            ";"
        ]

        return " ".join(string_parts)

    @staticmethod
    def __build_table(schema: str, table: str) -> str:
        """
        Convert a schema string and table string into a SQL table string.

        Args:
            schema (str): The schema the table belongs to.
            table (str): The name of the table.

        Returns:
            str: The SQL table string.

        Examples:
            - "example_schema"."example_table"
        """
        return f'"{schema}"."{table}"'

    def __build_columns(
            self,
            column_definitions: list[ColumnDefinition]) -> str:
        """
        Convert a list of ColumnDefinition objects into a SQL columns
        declaration string.

        Args:
            column_definitions (list[ColumnDefinition]): The ColumnDefinition
                objects to be converted.

        Returns:
            str: The SQL columns declaration string.

        Examples:
            - ("id" VARCHAR PRIMARY KEY, "petCount" INTEGER)
        """
        columns = [
            self.__build_column(definition)
            for definition in column_definitions
        ]

        return f"({', '.join(columns)})"

    @staticmethod
    def __build_column(column_definition: ColumnDefinition) -> str:
        """
        Convert a ColumnDefinition object into a SQL string.

        Args:
            column_definition (ColumnDefinition): The ColumnDefinition object
                to be converted.

        Returns:
            str: The SQL column declaration string.

        Examples:
            - "id" VARCHAR PRIMARY KEY
            - "petCount" INTEGER
        """
        if column_definition.primaryKey:
            return (f'"{column_definition.name}" '
                    f'{column_definition.dataType.value} '
                    f'PRIMARY KEY')

        return f'"{column_definition.name}" {column_definition.dataType.value}'
