from db_handler.db_handler.model.column_definition import ColumnDefinition
from db_handler.db_handler.model.table_definition import TableDefinition


class TableRequestBuilderFunction:

    def apply(self, table_definition: TableDefinition) -> str:
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
        return f'"{schema}"."{table}"'

    def __build_columns(
            self,
            column_definitions: list[ColumnDefinition]) -> str:
        return f"({', '.join(list(
            map(
                lambda definition:
                self.__build_column(definition),
                column_definitions
            )
        ))})"

    @staticmethod
    def __build_column(column_definition: ColumnDefinition) -> str:
        if column_definition.primaryKey:
            return (f'"{column_definition.name}" '
                    f'{column_definition.dataType.value} '
                    f'PRIMARY KEY')

        return f'"{column_definition.name}" {column_definition.dataType.value}'
