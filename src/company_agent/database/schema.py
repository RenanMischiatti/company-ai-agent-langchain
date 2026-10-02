from pathlib import Path

from company_agent.config import Settings
from company_agent.database.connection import create_database_connection


def initialize_database(settings: Settings) -> None:
    database_directory = Path(__file__).parent
    schema_sql = (database_directory / "schema.sql").read_text(
        encoding="utf-8"
    )
    seed_sql = (database_directory / "seed.sql").read_text(
        encoding="utf-8"
    )

    with create_database_connection(settings) as connection:
        connection.execute(schema_sql)
        connection.execute(seed_sql)
