from typing import Any

from fastapi import HTTPException

from db_handler.db_handler.model.column import Column
from db_handler.db_handler.model.query_condition import QueryCondition
from db_handler.db_handler.model.query_condition_group import QueryConditionGroup
from db_handler.db_handler.model.sql_query import SqlQuery
from db_handler.db_handler.model.table import Table
from db_handler.db_handler.model.table_join import TableJoin
from db_handler.db_handler.model.type.sql_operator import SqlOperator
from db_handler.db_handler.util.store_constants import StoreConstants


class QueryBuilderFunction:
    """
    Function for building SQL query strings from SqlQuery objects.
    """

    def apply(self, sql_query: SqlQuery) -> str:
        """
        Convert a SqlQuery object into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.

        Returns:
            str: The SQL query string.
        """
        string_parts: list[str] = [sql_query.operator.value]

        if sql_query.operator == SqlOperator.SELECT:
            string_parts = self.__build_select_statement(sql_query, string_parts)
        elif sql_query.operator == SqlOperator.INSERT:
            string_parts = self.__build_insert_statement(sql_query, string_parts)
        elif sql_query.operator == SqlOperator.UPDATE:
            string_parts = self.__build_update_statement(sql_query, string_parts)
        elif sql_query.operator == SqlOperator.DELETE:
            string_parts = self.__build_delete_statement(sql_query, string_parts)

        string_parts.append(";")

        return " ".join(string_parts)

    def __build_select_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        """
        Convert a SqlQuery object representing a SELECT query into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.
            string_parts (list[str]): The component parts of the SQL query string.

        Returns:
            str: The SQL SELECT query string.

        Examples:
            - SELECT * FROM example_schema.example_table ;
        """
        string_parts.append("*" if sql_query.columns is None else ", ".join(list(map(lambda column: self.__build_column(column, False), sql_query.columns))))
        string_parts.append("FROM")
        string_parts.append(self.__build_table(sql_query.table))

        if sql_query.tableJoins is not None and len(sql_query.tableJoins) > 0:
            string_parts.append(self.__build_table_joins(sql_query.tableJoins))

        if sql_query.conditionGroup is not None and len(sql_query.conditionGroup.conditions) > 0:
            string_parts.append("WHERE")
            string_parts.append(self.__build_conditions(sql_query.conditionGroup))

        return string_parts

    def __build_insert_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        """
        Convert a SqlQuery object representing an INSERT query into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.
            string_parts (list[str]): The component parts of the SQL query string.

        Returns:
            str: The SQL INSERT query string.

        Examples:
            - INSERT INTO example_schema.example_table (col1, col2) VALUES ('val1', 'val2'), (3, 4) ;
        """
        string_parts.append(self.__build_table(sql_query.table))

        columns: list[str] = sorted(list({key for rec in sql_query.records for key in rec}))
        string_parts.append(f"({', '.join(columns)})")

        string_parts.append("VALUES")
        string_parts.append(self.__build_insert_records(sql_query.records, columns))

        return string_parts

    def __build_update_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        """
        Convert a SqlQuery object representing an UPDATE query into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.
            string_parts (list[str]): The component parts of the SQL query string.

        Returns:
            str: The SQL UPDATE query string.

        Examples:
            - UPDATE test_schema.test_table SET col1 = CASE WHEN id = 'id1' THEN 'val1' ELSE col1 END WHERE id IN ('id1') ;
        """
        string_parts.append(self.__build_table(sql_query.table))

        string_parts.append("SET")
        string_parts.append(self.__build_set_clause(sql_query.records))

        return string_parts

    def __build_delete_statement(self, sql_query: SqlQuery, string_parts: list[str]) -> list[str]:
        """
        Convert a SqlQuery object representing a DELETE query into a SQL query string.

        Args:
            sql_query (SqlQuery): The SqlQuery object to be converted.
            string_parts (list[str]): The component parts of the SQL query string.

        Returns:
            str: The SQL DELETE query string.

        Examples:
            - DELETE FROM example_schema.example_table WHERE col1 = 'val1' ;
        """
        string_parts.append(self.__build_table(sql_query.table))

        string_parts.append("WHERE")
        string_parts.append(self.__build_conditions(sql_query.conditionGroup))

        return string_parts

    @staticmethod
    def __build_table(table: Table) -> str:
        """
        Convert a Table object into a SQL string.

        Args:
            table (Table): The Table object to be converted.

        Returns:
            str: The SQL table string.

        Examples:
            - example_schema.example_table
            - example_schema.example_table as example
        """
        if table.alias is None:
            return f"{table.schema_}.{table.table}"

        return f"{table.schema_}.{table.table} AS {table.alias}"

    def __build_table_joins(self, table_joins: list[TableJoin]) -> str:
        """
        Convert a list of TableJoin objects into a SQL string.

        Args:
            table_joins (list[TableJoin]): The list of TableJoin objects to be converted.

        Returns:
            str: The SQL table joins string.
        """
        join_strings: list[str] = list(map(lambda join: self.__build_table_join(join), table_joins))

        return " ".join(join_strings)

    def __build_table_join(self, table_join: TableJoin) -> str:
        """
        Convert a TableJoin object into a SQL string.

        Args:
            table_join (TableJoin): The TableJoin object to be converted.

        Returns:
            str: The SQL table join string.

        Examples:
            - INNER JOIN example_schema.join_table AS joiner ON example.id = joiner.id
        """
        return f"{table_join.joinType.value} {self.__build_table(table_join.table)} ON {self.__build_condition(table_join.joinCondition)}"

    def __build_conditions(self, query_condition_group: QueryConditionGroup) -> str:
        """
        Convert a QueryConditionGroup object into a SQL string.

        Args:
            query_condition_group (QueryConditionGroup): The QueryConditionGroup object to be converted.

        Returns:
            str: The SQL condition group string.

        Examples:
            - example.column1 = 'example' AND joiner.column2 < 23
        """
        condition_strings: list[str] = list(map(lambda condition: self.__build_condition(condition), query_condition_group.conditions))

        return f" {query_condition_group.join.value} ".join(condition_strings)

    def __build_condition(self, query_condition: QueryCondition) -> str:
        """
        Convert a QueryCondition object into a SQL string.

        Args:
            query_condition (QueryCondition): The QueryCondition object to be converted.

        Returns:
            str: The SQL condition string.

        Examples:
            - example.column1 = 'example'
            - joiner.column2 < 23
        """
        condition_parts: list[str] = [self.__build_column(query_condition.column, True), query_condition.operator.value]

        if query_condition.value is not None:
            condition_parts.append(self.__build_value(query_condition.value))

        return " ".join(condition_parts)

    def __build_value(self, value: Any) -> str:
        """
        Convert the value of a condition into a SQL string.

        Args:
            value (Any): The value to be converted.

        Returns:
            str: The SQL value string.

        Examples:
            - 'example'
            - 23
            - example_schema.example_table
        """
        if value == "NULL":
            return value

        if isinstance(value, str):
            return f"'{value}'"

        if isinstance(value, Column):
            return self.__build_column(value, True)

        return str(value)

    @staticmethod
    def __build_column(column: Column, is_condition: bool) -> str:
        """
        Convert a Column object into a SQL string.

        Args:
            column (Column): The Column object to be converted.
            is_condition (bool): True if the column belongs to a condition object.

        Returns:
            str: The SQL column string.

        Examples:
            - example_table.example_column
            - example_table.example_column AS example
        """
        if column.alias is not None and not is_condition:
            return f"{'.'.join(column.parts)} AS {column.alias}"

        return ".".join(column.parts)

    def __build_insert_records(self, records: list[dict[str, Any]], columns: list[str]) -> str:
        """
        Convert a list of records and insert columns into a SQL string.

        Args:
            records (list[dict[str, Any]]): The records to be converted.
            columns (list[str]): Columns to have values inserted to.

        Returns:
            str: The SQL insert records string.

        Examples:
            - ('val1', 2)
            - ('val3', 4), (5, 'val6')
        """
        return ", ".join(list(map(lambda record: self.__build_insert_record(record, columns), records)))

    def __build_insert_record(self, record: dict[str, Any], columns: list[str]) -> str:
        """
        Convert a record and insert columns into a SQL string.

        Args:
            record (dict[str, Any]): The record to be converted.
            columns (list[str]): Columns to have values inserted to.

        Returns:
            str: The SQL insert record string.

        Examples:
            - ('val1', 2)
        """
        values: list[str] = [self.__build_value(record.get(column, "NULL")) for column in columns]

        return f"({', '.join(values)})"

    def __build_set_clause(self, records: list[dict[str, Any]]) -> str:
        """
        Convert a list of records into a SQL SET clause string.

        Args:
            records (list[dict[str, Any]]): The records to be converted.

        Returns:
            str: The SQL SET clause string.

        Examples:
            - col1 = CASE WHEN id = 'id1' THEN 'val1' ELSE col1 END WHERE id IN ('id1')
            - col1 = CASE WHEN id = 'id1' THEN 'val1' ELSE col1, col2 = CASE WHEN id = 'id2' THEN 'val2' ELSE col2 END WHERE id IN ('id1', 'id2')
        """
        records_with_id: list[dict[str, Any]] = list(filter(lambda record: StoreConstants.ID in record, records))

        if len(records_with_id) < len(records):
            raise HTTPException(status_code=400, detail="All records in update requests should contain id field.")

        columns: list[str] = sorted(list({key for rec in records for key in rec}))
        columns.remove(StoreConstants.ID)

        case_clauses: list[str] = list(map(lambda column: self.__build_case_clause(column, records), columns))

        return (f"{', '.join(case_clauses)} WHERE {StoreConstants.ID} "
                f"IN ({', '.join(sorted(list({self.__build_value(item[StoreConstants.ID]) for item in records})))})")

    def __build_case_clause(self, column: str, records: list[dict[str, Any]]) -> str:
        """
        Convert a column and list of records into a SQL CASE clause string.

        Args:
            column (str): The column to be converted.
            records (list[dict[str, Any]]): The records to be converted.

        Returns:
            str: The SQL CASE clause string.

        Examples:
            - col1 = CASE WHEN id = 'id1' THEN 'val1' ELSE col1 END
        """
        filtered: list[dict[str, Any]] = list(filter(lambda record: column in record, records))

        return f"{column} = CASE {' '.join(list(map(lambda record: self.__build_when_clause(column, record), filtered)))} ELSE {column} END"

    def __build_when_clause(self, column: str, record: dict[str, Any]) -> str:
        """
        Convert a column and record into a SQL WHEN clause string.

        Args:
            column (str): The column to be converted.
            record (dict[str, Any]): The record to be converted.

        Returns:
            str: The SQL WHEN clause string.

        Examples:
            - WHEN id = 'id1' THEN 'val1'
        """
        return f"WHEN {StoreConstants.ID} = '{record[StoreConstants.ID]}' THEN {self.__build_value(record[column])}"
