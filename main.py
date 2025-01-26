from model.query_request import QueryRequest
from service.database_query_service import DatabaseQueryService


def main():
    database_query_service: DatabaseQueryService = DatabaseQueryService()

    query_request: QueryRequest = QueryRequest(schema="predictor", table="test")

    print(database_query_service.retrieve_records(query_request))

if __name__ == "__main__":
    main()