from predictor.model.query_request import QueryRequest
from predictor.model.sql_condition import SqlCondition
from predictor.model.sql_condition_group import SqlConditionGroup
from predictor.model.type.sql_condition_operator import SqlConditionOperator
from predictor.model.type.sql_join import SqlJoin
from predictor.service.database_query_service import DatabaseQueryService
from predictor.util.database_utils import DatabaseUtils


def main():
    database_query_service: DatabaseQueryService = DatabaseQueryService(DatabaseUtils.DATABASE_CONNECTION)

    query_request: QueryRequest = QueryRequest(
        schema="predictor",
        table="test",
        columns=["test", "hello"],
        conditionGroup=SqlConditionGroup(
            conditions=[
                SqlCondition(
                    column="test",
                    operator=SqlConditionOperator.EQUAL,
                    value="hello"
                ),
                SqlCondition(
                    column="hello",
                    operator=SqlConditionOperator.EQUAL,
                    value="goodbye"
                )
            ],
            join=SqlJoin.OR
        )
    )

    print(database_query_service.retrieve_records(query_request))

if __name__ == "__main__":
    main()