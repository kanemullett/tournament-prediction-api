from service.database_query_service import DatabaseQueryService


def main():
    database_query_service: DatabaseQueryService = DatabaseQueryService()

    database_query_service.test_connection()

if __name__ == "__main__":
    main()