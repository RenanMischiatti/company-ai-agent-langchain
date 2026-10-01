from pathlib import Path

from company_agent.config import Settings
from company_agent.database.connection import create_database_connection


def initialize_database(settings: Settings) -> None:
    schema_path = Path(__file__).with_name("schema.sql")
    schema_sql = schema_path.read_text(encoding="utf-8")

    with create_database_connection(settings) as connection:
        connection.execute(schema_sql)
