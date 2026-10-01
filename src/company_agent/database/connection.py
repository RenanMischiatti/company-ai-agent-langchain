import psycopg
from psycopg import Connection

from company_agent.config import Settings


def create_database_connection(settings: Settings) -> Connection:
    connection_url = settings.database_url.replace(
        "postgresql+psycopg://",
        "postgresql://",
        1,
    )
    return psycopg.connect(connection_url)
