import os
from psycopg2 import connect
from psycopg2._psycopg import cursor


class DatabaseQueryService:

    def __init__(self) -> None:
        self.__cursor = self.__get_cursor()

    @staticmethod
    def __get_cursor() -> cursor:
        try:
            connection = connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("POSTGRES_PORT")
            )

            return connection.cursor()

        except Exception as e:
            print("Error connecting to the database:", e)

    def test_connection(self):
        self.__cursor.execute("SELECT * FROM predictor.test;")
        rows = self.__cursor.fetchall()
        for row in rows:
            print(row)
